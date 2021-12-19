
# Default value 300 for earrings.
# 100 seems to work for watches
# Use 0 if its a pic from top left to bottom right. Use default if it's anything else.
# Offset 0 seems to look good with watches too
#OFFSETS = [100, 50, 0, -50, -100,]
class Args(object):

    def __init__(self,
                 padding=100,
                 add_left=100,
                 add_right=100,
                 add_top=5,
                 add_bot=2,
                 threshold=250,
                 dist=5,
                 pictures_dir_in="C:/Users/Karl/Projects/ThumbnailCreator/pics_to_resize/in/test/",
                 pictures_dir_out="C:/Users/Karl/Projects/ThumbnailCreator/resized_pics/out/test/",
                 temp_dir_out="C:/Users/Karl/AppData/Local/ThumbnailCreator/",
                 save_format=".png",
                 resize_size=(600, 600)
                 ):
        self.padding = padding
        self.add_left = add_left
        self.add_right = add_right
        self.add_top = add_top
        self.add_bot = add_bot
        self.threshold = threshold
        self.dist = dist
        self.pictures_dir_in = pictures_dir_in
        self.pictures_dir_out = pictures_dir_out
        self.temp_dir_out = temp_dir_out
        self.save_format = save_format
        self.resize = resize_size
