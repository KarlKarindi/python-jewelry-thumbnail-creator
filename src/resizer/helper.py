import os

def create_output_dir(input_dir):
    output_dir = input_dir + "600x600/"
    try:
        os.mkdir(output_dir)
    except:
        print("File already exists")
    return output_dir

def file_is_image(name):
    return name.lower().endswith(".jpg") or name.lower().endswith(".png")
