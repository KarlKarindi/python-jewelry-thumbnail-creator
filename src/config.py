
# Default value 300 for earrings.
# 100 seems to work for watches
# Use 0 if its a pic from top left to bottom right. Use default if it's anything else.
# Offset 0 seems to look good with watches too
#OFFSETS = [100, 50, 0, -50, -100,]
PADDINGS = [700]


# Set threshold to 100 if it's a self-made picture
THRESHOLD = 250  # Option either 250 or whatever

DIST = 5

# # Append / after every folder
PICTURES_DIRS_IN = [
                   "C:/Users/Karl/Projects/picture_resizer/pics_to_resize/in/Kameele pildid/"
                   ]

# Must add folder to save as well if it doesn't exist;
""" PICTURES_DIRS_OUT = [
                    "C:/Users/Karl/Projects/picture_resizer/resized_pics/out/zoom_-100/",
                    "C:/Users/Karl/Projects/picture_resizer/resized_pics/out/zoom_-50/",
                    "C:/Users/Karl/Projects/picture_resizer/resized_pics/out/zoom_0/",
                    "C:/Users/Karl/Projects/picture_resizer/resized_pics/out/zoom_50/",
                    "C:/Users/Karl/Projects/picture_resizer/resized_pics/out/zoom_100/",
                    ]
 
"""
 
PICTURES_DIRS_OUT = "C:/Users/Karl/Projects/picture_resizer/resized_pics/out/test/",
 
TEMP_DIR_OUT = "C:/Users/Karl/AppData/Local/picture_resizer/"
SAVE_FORMAT = ".png"

RESIZE_SIZE = (600, 600)