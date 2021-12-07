
# Default value 300 for earrings.
# 100 seems to work for watches
# Use 0 if its a pic from top left to bottom right. Use default if it's anything else.
# Offset 0 seems to look good with watches too
OFFSET = 125


# Set threshold to 100 if it's a self-made picture
THRESHOLD = 250  # Option either 250 or whatever
USE_DIST = False
DIST = 5

# # Append / after every folder
PICTURES_DIRS_IN = [
                   "C:/Users/Karl/Projects/picture_resizer/pics_to_resize/last/"
                   ]
# Must add folder to save as well if it doesn't exist;
PICTURES_DIRS_OUT = [
                    "C:/Users/Karl/Projects/picture_resizer/resized_pics/"
                    ]

TEMP_DIR_OUT = "C:/Users/Karl/AppData/Local/picture_resizer/"
SAVE_FORMAT = ".png"
