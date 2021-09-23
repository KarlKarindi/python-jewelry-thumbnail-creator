from PIL import Image
from config import PICTURES_DIR_OUT, PICTURES_DIR_IN, TEMP_DIR_OUT, TEMP_DIR, THRESHOLD, DIST, USE_DIST, OFFSET, SAVE_FORMAT
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob


def start():
    pic_files = [f for f in listdir(PICTURES_DIR_IN)
                 if isfile(join(PICTURES_DIR_IN, f))]

    print("Starting the resizing process!")
    print("Save location:", PICTURES_DIR_OUT, '\n')
    pic_count = 0
    for pic_name in pic_files:
        if pic_name.lower().endswith(".jpg") or pic_name.lower().endswith(".png"):
            pic_count += 1
            pic_name_without_jpg = pic_name[:pic_name.rindex(".")]

            og_img = Image.open(PICTURES_DIR_IN + pic_name)
            bg_rgb = find_rgb_of_og_img_bg(og_img)
            
            w = og_img.width
            h = og_img.height

            bigger_dimension = w
            if w > h:
                additional = (w - h)
            else:
                additional = (h - w)
                bigger_dimension = h


            background = Image.new('RGB', (additional + bigger_dimension,
                                           additional + bigger_dimension), (bg_rgb[0], bg_rgb[1], bg_rgb[2]))
            bg_w, bg_h = background.size
            paste_to_background(og_img, background, bg_w,
                                bg_h, pic_name_without_jpg)

            img_with_background = Image.open(
                TEMP_DIR_OUT + "OUT_" + pic_name_without_jpg + ".png")
            pixels = img_with_background.load()
            cropped_img = crop_image(img_with_background, pixels)

            resize(cropped_img, pic_name_without_jpg + SAVE_FORMAT)

            print("Resized picture #" + str(pic_count) + ":", pic_name,
                  og_img.size, "- Saved as:", pic_name_without_jpg + SAVE_FORMAT)

    print("\nResizing completed!")
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


def resize(cropped_img, pic_name):
    new_img = cropped_img.resize((600, 600))
    new_img.save(PICTURES_DIR_OUT + pic_name, optimize=True)


def crop_image(img, pixels):
    w, h = img.width - 1, img.height - 1

    x_min = find_x_min(pixels, w, h)
    x_max = find_x_max(pixels, w, h)
    y_min = find_y_min(pixels, x_min, x_max, h)
    y_max = find_y_max(pixels, x_min, x_max, h)
    
    crop_info = CropInfo(
        x_min,
        x_max,
        y_min,
        y_max,
        )

    w = crop_info.X_MAX - crop_info.X_MIN
    h = crop_info.Y_MAX - crop_info.Y_MIN

    crop_info = fix_incorrect_aspect_ratio(crop_info, w, h)
    cropped_img = img.crop(
        (crop_info.X_MIN, crop_info.Y_MIN, crop_info.X_MAX, crop_info.Y_MAX))
    return cropped_img

def find_x_min(pixels, w, h):
    for x in range(w):
        for y in range(h):
            if not pixel_is_white(pixels[x, y]):
                return x

def find_x_max(pixels, w, h):
    for x in reversed(range(w)):
        for y in range(h):
            if not pixel_is_white(pixels[x, y]):
                return x

def find_y_min(pixels, w_start, w_end, h):
    for y in range(h):
        for x in range(w_start, w_end):
            if not pixel_is_white(pixels[x, y]):
                return y

def find_y_max(pixels, w_start, w_end, h):
    for y in reversed(range(h)):
        for x in range(w_start, w_end):
            if not pixel_is_white(pixels[x, y]):
                return y

def fix_incorrect_aspect_ratio(info, w, h):
    if w > h:
        offset = (w - h) / 2
        info.Y_MIN -= offset
        info.Y_MAX += offset
    else:
        offset = (h - w) / 2
        info.X_MIN -= offset
        info.X_MAX += offset

    crop_width = info.X_MAX - info.X_MIN
    x_offset_extra = 0
    if crop_width < 600:
        x_offset_extra = (600 - crop_width) / 2
    info.X_MIN -= (OFFSET + x_offset_extra)
    info.X_MAX += (OFFSET + x_offset_extra)

    crop_height = info.Y_MAX - info.Y_MIN
    y_offset_extra = 0
    if crop_height < 600:
        y_offset_extra = (600 - crop_height) / 2
    info.Y_MIN -= (OFFSET + y_offset_extra)
    info.Y_MAX += (OFFSET + y_offset_extra)

    return info


def pixel_is_white(pixel):
    r, g, b = pixel[0], pixel[1], pixel[2]
    first_test_pass = ((r >= THRESHOLD)
                       and (g >= THRESHOLD)
                       and (b >= THRESHOLD))

    if not USE_DIST:
        return first_test_pass

    # this takes a lot more time for negligible difference
    return ((np.abs(r - g) < DIST)
            and (np.abs(r - b) < DIST)
            and (np.abs(g - b) < DIST))


def paste_to_background(img, background, bg_w, bg_h, img_name):
    img_w, img_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    background.save(TEMP_DIR_OUT + "OUT_" + img_name + ".png")


def find_rgb_of_og_img_bg(img):
    pixels = img.load()
    width, height = img.width, img.height
    for x in range(0, width):
        for y in range(0, height):
            pixel = pixels[x, y]
            if pixel_is_white(pixel):
                return pixel

start()
