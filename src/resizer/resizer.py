from PIL import Image
from resizer.args import Args
from os import listdir
from os.path import isfile, join
import numpy as np
import os
import glob
import time
import cv2


def handleArgs(args):
    if args.do_reflection_removal:
        args.canny_min_threshold, args.canny_max_threshold = 100, 200
        args.add_left, args.add_right, args.add_top, args.add_bottom = 10, 10, 10, 10
    else:
        args.canny_min_threshold, args.canny_max_threshold = 0, 0
        args.add_left, args.add_right, args.add_top, args.add_bottom = 100, 100, 5, 2
    return args


def execute(args):
    files = [f for f in listdir(args.pictures_dir_in)
             if isfile(join(args.pictures_dir_in, f))]

    args = handleArgs(args)

    print("Save format:", args.save_format,
          "- Save location:", args.pictures_dir_out)
    pic_count = 0
    process_start_time = time.time()
    for name in files:
        if file_is_image(name):
            start_time = time.time()
            pic_count += 1
            abspath = args.pictures_dir_in + name

            ci = find_crop_coords(abspath, args)
            img = Image.open(abspath)
            original_size = img.size

            # Do the initial crop so that only the piece of jewelerry remains. Reflection is removed
            img = img.crop((ci.X_MIN, ci.Y_MIN, ci.X_MAX, ci.Y_MAX))
            img = add_padding(remove_black_borders(img), args)
            img = img.resize((600, 600))
            img.save(args.pictures_dir_out + name, optimize=True)

            print("Resized picture #" + str(pic_count) + ":", name,
                  original_size, "- time taken:", np.round(time.time() - start_time, 3))

    print("Resizing completed!")
    delete_temp_files(files, args.temp_dir_out)
    return time.time() - process_start_time


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


def delete_temp_files(files, temp_dir_out):
    print("Deleting all temporary files...")
    files = glob.glob(temp_dir_out + "/*.png")
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    print("Deleting temporary files completed!")


# for input in PICTURES_DIRS_IN:
 #   for i, output in enumerate(PICTURES_DIRS_OUT):
  #      PADDING = PADDINGS[i]
   #     execute(input, output)
