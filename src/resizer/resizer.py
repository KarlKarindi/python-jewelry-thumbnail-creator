from PIL import Image
from resizer.args import Args
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob
import time
import cv2
from src.resizer import helper


class ResizeResult(object):

    def __init__(self, file_name, original_size, spent_time):
        self.file_name = file_name
        self.original_size = original_size
        self.spent_time = np.round(spent_time, 3)

    def __str__(self):
        return "spent time: {}, original_size: {}, file name: {}".format(self.spent_time, self.original_size, self.file_name)


def handleArgs(args):
    if args.do_reflection_removal:
        args.canny_min_threshold, args.canny_max_threshold = 100, 200
        args.add_left, args.add_right, args.add_top, args.add_bottom = 100, 100, 30, 5
    else:
        args.canny_min_threshold, args.canny_max_threshold = 0, 0
        args.add_left, args.add_right, args.add_top, args.add_bottom = 100, 100, 5, 2
    return args


def setup(input_dirs, args):

    input_dirs = helper.fix_input_dirs_names(input_dirs)
    output_dirs = helper.create_output_dirs(input_dirs)
    img_file_names = helper.create_img_file_names(input_dirs)
    total_picture_count = helper.count_total_pictures(img_file_names)
    args = handleArgs(args)

    return list(zip(input_dirs, output_dirs, img_file_names)), args, total_picture_count


def resize_img(img_abspath, save_loc, args):
    start_time = time.time()
    ci = find_crop_coords(img_abspath, args)
    img = Image.open(img_abspath)
    original_size = img.size

    # Do the initial crop so that only the piece of jewelerry remains. Reflection is removed
    img = img.crop((ci.X_MIN, ci.Y_MIN, ci.X_MAX, ci.Y_MAX))
    img = add_padding(remove_black_borders(img), args)
    img = img.resize((600, 600))
    img.save(save_loc, optimize=True)

    return ResizeResult(
        spent_time=time.time() - start_time,
        file_name=save_loc,
        original_size=original_size
    )


def find_crop_coords(abspath, args):
    img = cv2.imread(abspath)

    edges = cv2.Canny(img, args.canny_min_threshold, args.canny_max_threshold)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv += 500
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    indices = np.nonzero(edges)

    ci = CropInfo(
        min(indices[1]) - args.add_left,
        max(indices[1]) + args.add_right,
        min(indices[0]) - args.add_top,
        max(indices[0]) + args.add_bot
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


def add_padding(img, args):
    width = img.size[0]
    height = img.size[1]
    if width != height:
        bigger_side = width if width > height else height
        bg = Image.new('RGB', (bigger_side + args.padding,
                               bigger_side + args.padding), (255, 255, 255))
        offset = ((bigger_side - width + args.padding) // 2,
                  (bigger_side - height + args.padding) // 2)
        bg.paste(img, offset)
        return bg
    return img


def remove_black_borders(img):
    pix = np.array(img)
    
    black, white = get_black_and_white_value(pix.shape[-1] == 4)
        
    print(pix.shape, black.shape, white.shape)

    pix2 = pix.copy()
    dim = pix.shape

    for n in range(dim[0]):
        if (pix[n, :] == black).all():
            pix2[n, :] = white

    for n in range(dim[1]):
        if (pix[:, n] == black).all():
            pix2[:, n] = white

    return Image.fromarray(pix2)

def get_black_and_white_value(img_is_rgba):
    if img_is_rgba:
        return np.array([0, 0, 0, 0]), np.array([255, 255, 255, 0])
    return np.array([0, 0, 0]), np.array([255, 255, 255])