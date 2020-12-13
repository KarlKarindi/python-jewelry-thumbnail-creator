from PIL import Image
from os import listdir
from os.path import isfile, join

pictures_dir = "C:/Users/Karl/Desktop/wetransfer-8d7bb4/08.12.2020/"
new_pictures_dir = "C:/Users/Karl/Desktop/EhetePildidVaiksemad2/"
pic_files = [f for f in listdir(pictures_dir) if isfile(join(pictures_dir, f))]


class CropInfo(object):
    X_MIN = 999999
    X_MAX = -1
    Y_MIN = 999999
    Y_MAX = -1

    def __str__(self):
        return str(self.X_MIN) + " " + str(self.X_MAX) + " " + str(self.Y_MIN) + " " + str(self.Y_MAX)

def resize(pic_files):
    for pic_name in pic_files:
        if pic_name.endswith(".jpg"):
            original_img = Image.open(pictures_dir + pic_name)
            cropped_img = crop_image(original_img)
            if cropped_img.width < 600:
                print(cropped_img.size, pic_name)
            new_img = cropped_img.resize((600, 600))
            new_img.save(new_pictures_dir + pic_name, "JPEG", optimize=True)

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
    
    cropped_img = img.crop((crop_info.X_MIN, crop_info.Y_MIN, crop_info.X_MAX, crop_info.Y_MAX))
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
    offset = 150
    x_offset_extra = 0
    if crop_width < 600:
        x_offset_extra = (600 - crop_width) / 2
    info.X_MIN -= (offset + x_offset_extra)
    info.X_MAX += (offset + x_offset_extra)
    
    crop_height = info.Y_MAX - info.Y_MIN
    y_offset_extra = 0
    if crop_height < 600:
        y_offset_extra = (600 - crop_height) / 2
    info.Y_MIN -= (offset + y_offset_extra)
    info.Y_MAX += (offset + y_offset_extra)

    return info

def pixel_is_white(pixel):
    return pixel == (255, 255, 255) or pixel == (254, 254, 254)

print("Resizing", len(pic_files), "pictures")
resize(pic_files)
print("Resizing completed")
