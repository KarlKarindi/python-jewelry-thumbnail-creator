from PIL import Image
from os import listdir
from os.path import isfile, join



class CropInfo(object):
    X_MIN = 999999
    X_MAX = -1
    Y_MIN = 999999
    Y_MAX = -1

    def __str__(self):
        return "X_MIN: {}, X_MAX: {}, Y_MIN: {}, Y_MAX: {}".format(self.X_MIN, self.X_MAX, self.Y_MIN, self.Y_MAX)

def resize(cropped_img, pic_name):
    new_img = cropped_img.resize((600, 600))
    new_img.save(PICTURES_DIR_OUT + pic_name.strip(".jpg") + ".png", optimize=True)

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
    
    # print(crop_info)
    
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
    offset = 100
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
    return pixel == (255, 255, 255) or pixel == (254, 254, 254) or pixel == (253, 253, 253)

def paste_to_background(img, background, bg_w, bg_h, img_name):
    img_w, img_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    background.save(TEMP_DIR_OUT + "OUT_" + img_name + ".png")
    

#PICTURES_DIR_IN = "C:/Users/Karl/Desktop/wetransfer-8d7bb4/08.12.2020/"
PICTURES_DIR_IN = "C:/Users/Karl/Desktop/test/"
PICTURES_DIR_OUT = "C:/Users/Karl/Desktop/OUT_Pildid/"
TEMP_DIR = "C:/Users/Karl/Desktop/resizing/"
TEMP_DIR_OUT = "C:/Users/Karl/Desktop/resizing/out/"
pic_files = [f for f in listdir(PICTURES_DIR_IN) if isfile(join(PICTURES_DIR_IN, f))]

background = Image.new('RGB', (2500, 2500), (255, 255, 255))
bg_w, bg_h = background.size
print("Resizing", len(pic_files), "pictures\n")

for pic_name in pic_files:
    if pic_name.endswith(".jpg"):
        #print("Resizing picture", pic_name)
        pic_name_without_jpg = pic_name.strip(".jpg")
        original_img = Image.open(PICTURES_DIR_IN + pic_name)
        paste_to_background(original_img, background, bg_w, bg_h, pic_name_without_jpg)
        img_with_background = Image.open(TEMP_DIR_OUT + "OUT_" + pic_name_without_jpg + ".png")
        cropped_img = crop_image(img_with_background)
        resize(cropped_img, pic_name)
        #print()

print("Resizing completed")
