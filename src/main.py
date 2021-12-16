from PIL import Image, ImageChops
from config import PICTURES_DIRS_OUT, PICTURES_DIRS_IN, TEMP_DIR_OUT, THRESHOLD, PADDINGS, SAVE_FORMAT, RESIZE_SIZE
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob
import time

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
            img = Image.open(pictures_dir_in + name)
            original_size = img.size
            img = add_padding(remove_black_borders(crop_img(img)))
            img = img.resize((600, 600))
            img.save(pictures_dir_out + name, optimize=True)

            print("Resized picture #" + str(pic_count) + ":", name,
                  original_size, "- time taken:", np.round(time.time() - start_time, 3))

    print("Resizing completed!")
    print("Process completed in:", np.round(time.time() - process_start_time, 3), "seconds")
    delete_temp_files(files)


class CropInfo(object):
    def __init__(self, X_MIN, X_MAX, Y_MIN, Y_MAX):
        self.X_MIN = X_MIN
        self.X_MAX = X_MAX
        self.Y_MIN = Y_MIN
        self.Y_MAX = Y_MAX

    def __str__(self):
        return "X_MIN: {}, X_MAX: {}, Y_MIN: {}, Y_MAX: {}".format(self.X_MIN, self.X_MAX, self.Y_MIN, self.Y_MAX)


def crop_img(img):
    w, h = img.width, img.height
    imgnp = np.array(img)
    elem_width = (max(np.where(imgnp < THRESHOLD)[
                  1])) - (min(np.where(imgnp < THRESHOLD)[1]))
    elem_height = (max(np.where(imgnp < THRESHOLD)[
                   0])) - (min(np.where(imgnp < THRESHOLD)[0]))

    x_mid, y_mid = w / 2, h / 2
    x_min = x_mid - (elem_width / 2)
    x_max = x_mid + (elem_width / 2)
    y_min = y_mid - (elem_height / 2)
    y_max = y_mid + (elem_height / 2)

    ci = CropInfo(
        x_min,
        x_max,
        y_min,
        y_max,
    )

    w = ci.X_MAX - ci.X_MIN
    h = ci.Y_MAX - ci.Y_MIN

    ci = fix_incorrect_aspect_ratio(ci, w, h)
    cropped_img = img.crop(
        (ci.X_MIN, ci.Y_MIN, ci.X_MAX, ci.Y_MAX))

    return cropped_img


def fix_incorrect_aspect_ratio(ci, w, h):
    if w > h:
        offset = (w - h) / 2
        ci.Y_MIN -= offset
        ci.Y_MAX += offset
    else:
        offset = (h - w) / 2
        ci.X_MIN -= offset
        ci.X_MAX += offset

    return ci


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


def pixel_is_white(pixel):
    r, g, b = pixel[0], pixel[1], pixel[2]
    return ((r >= THRESHOLD)
            and (g >= THRESHOLD)
            and (b >= THRESHOLD))


def add_padding(img):
    bg = Image.new('RGB', (img.size[0] + OFFSET, img.size[1] + OFFSET), (255, 255, 255))
    offset = (OFFSET // 2, OFFSET // 2)
    bg.paste(img, offset)
    return bg


def file_is_image(name):
    return name.lower().endswith(".jpg") or name.lower().endswith(".png")


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
        OFFSET = PADDINGS[i]
        execute(input, output)
