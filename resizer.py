from PIL import Image
from config import PICTURES_DIR_OUT, PICTURES_DIR_IN, TEMP_DIR_OUT, TEMP_DIR, THRESHOLD, DIST, USE_DIST, OFFSET, WHITE_BG_ADDITIONAL, SAVE_FORMAT
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob


class CropInfo(object):
    X_MIN = 999999
    X_MAX = -1
    Y_MIN = 999999
    Y_MAX = -1

    def __str__(self):
        return "X_MIN: {}, X_MAX: {}, Y_MIN: {}, Y_MAX: {}".format(self.X_MIN, self.X_MAX, self.Y_MIN, self.Y_MAX)


def resize(cropped_img, pic_name):
    new_img = cropped_img.resize((600, 600))
    new_img.save(PICTURES_DIR_OUT + pic_name, optimize=True)


def crop_image(img):
    pixels = img.load()
    width, height = img.width - 1, img.height - 1

    crop_info = CropInfo()
    for x in range(0, width):
        for y in range(0, height):
            pixel = pixels[x, y]
            if not pixel_is_white(pixel):
                crop_info = extract_info(crop_info, x, y)

    width = crop_info.X_MAX - crop_info.X_MIN
    height = crop_info.Y_MAX - crop_info.Y_MIN

    crop_info = fix_incorrect_aspect_ratio(crop_info, width, height)
    cropped_img = img.crop(
        (crop_info.X_MIN, crop_info.Y_MIN, crop_info.X_MAX, crop_info.Y_MAX))
    return cropped_img


def extract_info(crop_info, x, y):
    if x < crop_info.X_MIN:
        crop_info.X_MIN = x
    if x > crop_info.X_MAX:
        crop_info.X_MAX = x
    if y < crop_info.Y_MIN:
        crop_info.Y_MIN = y
    if y > crop_info.Y_MAX:
        crop_info.Y_MAX = y
    return crop_info


def fix_incorrect_aspect_ratio(info, width, height):
    if width > height:
        offset = (width - height) / 2
        info.Y_MIN -= offset
        info.Y_MAX += offset
    else:
        offset = (height - width) / 2
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


pic_files = [f for f in listdir(PICTURES_DIR_IN)
             if isfile(join(PICTURES_DIR_IN, f))]

print("Starting the resizing process!")
print("Save location:", PICTURES_DIR_OUT, '\n')
pic_count = 0
for pic_name in pic_files:
    if pic_name.lower().endswith(".jpg") or pic_name.lower().endswith(".png"):
        pic_count += 1
        last_period_index = pic_name.rindex(".")
        pic_name_without_jpg = pic_name[:last_period_index]

        original_img = Image.open(PICTURES_DIR_IN + pic_name)

        original_img_width = original_img.width
        background = Image.new('RGB', (WHITE_BG_ADDITIONAL + original_img_width,
                                       WHITE_BG_ADDITIONAL + original_img_width), (255, 255, 255))
        bg_w, bg_h = background.size
        paste_to_background(original_img, background, bg_w,
                            bg_h, pic_name_without_jpg)
        img_with_background = Image.open(
            TEMP_DIR_OUT + "OUT_" + pic_name_without_jpg + ".png")
        cropped_img = crop_image(img_with_background)
        resize(cropped_img, pic_name_without_jpg + SAVE_FORMAT)

        print("Resized picture #" + str(pic_count) + ":", pic_name,
              original_img.size, "- Saved as:", pic_name_without_jpg + SAVE_FORMAT)

print("Resizing completed!")
print("Deleting all temporary files...")
files = glob.glob(TEMP_DIR_OUT + "/*.png")
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))
print("Deleting temporary files completed!")
