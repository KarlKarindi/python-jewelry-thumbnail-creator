from PIL import Image
from config import PICTURES_DIRS_OUT, PICTURES_DIRS_IN, TEMP_DIR_OUT, THRESHOLD, OFFSETS, SAVE_FORMAT
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob
import time


def start_resize(pictures_dir_in, pictures_dir_out):
    pic_files = [f for f in listdir(pictures_dir_in)
                 if isfile(join(pictures_dir_in, f))]

    print("\nStarting the resizing process!")
    print("Save location:", pictures_dir_out)
    pic_count = 0
    for pic_name in pic_files:
        if pic_name.lower().endswith(".jpg") or pic_name.lower().endswith(".png"):
            pic_count += 1
            pic_name_without_jpg = pic_name[:pic_name.rindex(".")]

            og_img = Image.open(pictures_dir_in + pic_name)

            cropped_img = crop_image(og_img)

            bg_added_img = paste_to_background(
                cropped_img)
            new_img = bg_added_img.resize((600, 600))
            new_img.save(pictures_dir_out + pic_name, optimize=True)

            print("Resized picture #" + str(pic_count) + ":", pic_name,
                  og_img.size, "- Saved as:", pic_name_without_jpg + SAVE_FORMAT)

    print("Resizing completed!")
    print("Deleting all temporary files...")
    files = glob.glob(TEMP_DIR_OUT + "/*.png")
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    print("Deleting temporary files completed!")


class CropInfo(object):
    def __init__(self, X_MIN, X_MAX, Y_MIN, Y_MAX):
        self.X_MIN = X_MIN
        self.X_MAX = X_MAX
        self.Y_MIN = Y_MIN
        self.Y_MAX = Y_MAX

    def __str__(self):
        return "X_MIN: {}, X_MAX: {}, Y_MIN: {}, Y_MAX: {}".format(self.X_MIN, self.X_MAX, self.Y_MIN, self.Y_MAX)


def crop_image(img):
    w, h = img.width, img.height
    imgnp = np.array(img)
    elem_width = (max(np.where(imgnp < THRESHOLD)[
                  1])) - (min(np.where(imgnp < THRESHOLD)[1]))
    elem_height = (max(np.where(imgnp < THRESHOLD)[
                   0])) - (min(np.where(imgnp < THRESHOLD)[0]))

    x_mid, y_mid = w / 2, h / 2
    n_x_min = x_mid - (elem_width / 2)
    n_x_max = x_mid + (elem_width / 2)
    n_y_min = y_mid - (elem_height / 2)
    n_y_max = y_mid + (elem_height / 2)

    crop_info = CropInfo(
        n_x_min,
        n_x_max,
        n_y_min,
        n_y_max,
    )

    w = crop_info.X_MAX - crop_info.X_MIN
    h = crop_info.Y_MAX - crop_info.Y_MIN

    crop_info = fix_incorrect_aspect_ratio(crop_info, w, h)
    cropped_img = img.crop(
        (crop_info.X_MIN, crop_info.Y_MIN, crop_info.X_MAX, crop_info.Y_MAX))
    

    return cropped_img


def fix_incorrect_aspect_ratio(info, w, h):
    if w > h:
        offset = (w - h) / 2
        info.Y_MIN -= offset
        info.Y_MAX += offset
    else:
        offset = (h - w) / 2
        info.X_MIN -= offset
        info.X_MAX += offset
        
    print("w", w, "h", h)
    print(info)
    # TODO: PROBLEM HERE WITH BLACK BOXES
    return info


def pixel_is_white(pixel):
    r, g, b = pixel[0], pixel[1], pixel[2]
    return ((r >= THRESHOLD)
            and (g >= THRESHOLD)
            and (b >= THRESHOLD))


def paste_to_background(img):
    background = Image.new('RGB', (600 + OFFSET,
                                   600 + OFFSET), (255, 255, 255))
    img_w, img_h = img.size
    offset = ((600 + OFFSET - img_w) // 2, (600 + OFFSET - img_h) // 2)
    background.paste(img, offset)
    return background


def find_rgb_of_og_img_bg(img):
    pixels = img.load()
    width, height = img.width, img.height
    for x in range(0, width):
        for y in range(0, height):
            pixel = pixels[x, y]
            if pixel_is_white(pixel):
                return pixel
    return (0, 0, 0)


for _in in PICTURES_DIRS_IN:
    for i, _out in enumerate(PICTURES_DIRS_OUT):
        OFFSET = OFFSETS[i]
        start_resize(_in, _out)
