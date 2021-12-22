from os import listdir
from os.path import isfile, join
import os


def fix_input_dirs_names(input_dirs):
    fixed = []
    for idir in input_dirs:
        if not idir.endswith("/"):
            idir += "/"
        fixed.append(idir)
    return fixed

def create_output_dirs(input_dirs):
    output_dirs = []
    for idir in input_dirs:
        output_dir = idir + "600x600/"
        output_dirs.append(output_dir)
        try:
            os.mkdir(output_dir)
        except:
            print("Output directory already exists for", idir)

    return output_dirs


def create_img_file_names(input_dirs):
    img_file_names = []
    for idir in input_dirs:
        result = [f for f in listdir(idir)
                  if isfile(join(idir, f)) and file_is_image(f)]
        img_file_names.append(result)
    return img_file_names

def file_is_image(name):
    return name.lower().endswith(".jpg") or name.lower().endswith(".png")
