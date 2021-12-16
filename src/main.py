from PIL import Image, ImageChops
from config import PICTURES_DIRS_OUT, PICTURES_DIRS_IN, TEMP_DIR_OUT, THRESHOLD, PADDINGS, SAVE_FORMAT, RESIZE_SIZE
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob
import time
import cv2
from matplotlib import pyplot as plt


def execute(pictures_dir_in, pictures_dir_out):
    files = [f for f in listdir(pictures_dir_in)
             if isfile(join(pictures_dir_in, f))]

    print("Starting the resizing process!")
    print("Save format:", SAVE_FORMAT, "- Save location:", pictures_dir_out)
    pic_count = 0
    process_start_time = time.time()
    for name in files:
        if file_is_image(name):
            start_time = time.time()
            pic_count += 1
            abspath = pictures_dir_in + name

            ci = find_crop_coords(abspath)
            img = Image.open(abspath)
            original_size = img.size
            
            # Do the initial crop so that only the piece of jewelerry remains. Reflection is removed
            img = img.crop((ci.X_MIN, ci.Y_MIN, ci.X_MAX, ci.Y_MAX))
            img = add_padding(remove_black_borders(img))
            img = img.resize((600, 600))
            img.save(pictures_dir_out + name, optimize=True)

            print("Resized picture #" + str(pic_count) + ":", name,
                  original_size, "- time taken:", np.round(time.time() - start_time, 3))

    print("Resizing completed!")
    print("Process completed in:", np.round(
        time.time() - process_start_time, 3), "seconds")
    delete_temp_files(files)


def find_crop_coords(abspath):
    img = cv2.imread(abspath)
    original = img.copy()
    img_blur = cv2.blur(img, (5,5))   
    #edges = cv.Canny(img, 60, 50)
    mask = np.zeros(img.shape, dtype=np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 10, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        cv2.drawContours(mask, [c], -1, (255,255,255), -1)
        break

    close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=4)
    close = cv2.cvtColor(close, cv2.COLOR_BGR2GRAY)
    result = cv2.bitwise_and(original, original, mask=close)
    result[close==0] = (255,255,255)

    cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('custom window', result)
    cv2.resizeWindow('custom window', 800  , 800)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    #indices = np.where(edges != [0])

    indices = np.nonzero(thresh)
    
    ci = CropInfo(
        min(indices[1]) - 250,
        max(indices[1]) + 250,
        min(indices[0]) - 250,
        max(indices[0]) + 5
    )
    return ci


class CropInfo(object):
    def __init__(self, X_MIN, X_MAX, Y_MIN, Y_MAX):
        self.X_MIN = X_MIN
        self.X_MAX = X_MAX
        self.Y_MIN = Y_MIN
        self.Y_MAX = Y_MAX

    def __str__(self):
        return "X_MIN: {}, X_MAX: {}, Y_MIN: {}, Y_MAX: {}".format(self.X_MIN, self.X_MAX, self.Y_MIN, self.Y_MAX)

def add_padding(img):
    width = img.size[0]
    height = img.size[1]
    if width != height:
        bigger_side = width if width > height else height
        bg = Image.new('RGB', (bigger_side + PADDING,
                               bigger_side + PADDING), (255, 255, 255))
        offset = ((bigger_side - width + PADDING) // 2, (bigger_side - height + PADDING) // 2)
        bg.paste(img, offset)
        return bg
    return img


def file_is_image(name):
    return name.lower().endswith(".jpg") or name.lower().endswith(".png")


def remove_black_borders(img):
    pix = np.array(img)
    black = np.array([0, 0, 0])
    white = np.array([255, 255, 255])

    pix2 = pix.copy()
    dim = pix.shape

    for n in range(dim[0]):
        if (pix[n, :] == black).all():
            pix2[n, :] = white

    for n in range(dim[1]):
        if (pix[:, n] == black).all():
            pix2[:, n] = white

    return Image.fromarray(pix2)



def delete_temp_files(files):
    print("Deleting all temporary files...")
    files = glob.glob(TEMP_DIR_OUT + "/*.png")
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    print("Deleting temporary files completed!")


for input in PICTURES_DIRS_IN:
    for i, output in enumerate(PICTURES_DIRS_OUT):
        PADDING = PADDINGS[i]
        execute(input, output)
