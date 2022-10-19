# script that sorts wallpapers into folders depending on
# whether they're desktop wallpapers (landscape orientation) or mobile wallpapers (portrait orientation)

# argument parser to get the path to the wallpapers folder
# if no path is given, the current directory is used
import argparse
from http.client import SWITCHING_PROTOCOLS
parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to wallpapers folder", nargs='?', default='.')
# add recursive option
parser.add_argument("-r", "--recursive", help="search for wallpapers in subfolders", action="store_true")
# add option to sort wallpapers by brightness level (into dark and light folders)
parser.add_argument("-b", "--brightness", help="sort wallpapers by brightness level in addition to orientation", action="store_true")
args = parser.parse_args()

# import the necessary packages
from PIL import Image
import os

# get the path to the wallpapers folder
path = args.path

# check if the path is valid
# if not, print error message and exit
if not os.path.isdir(path):
    print("Error: invalid path")
    exit()

# check if the user the script is running as can write to the directory
# if not, print error message and exit
if not os.access(path, os.W_OK):
    print("Error: cannot write to directory")
    exit()


# function for getting the list of image files in a directory
# if the recursive option is set, it will also search subdirectories
# ignore 'desktop' and 'mobile' folders if boolean ignore_script_folders is set to True
def get_images(path, recursive, ignore_script_folders):
    # list of image file extensions
    extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    # list of image files
    images = []
    # if the recursive option is set, search subdirectories
    if recursive:
        # walk through the directory tree
        # ignore 'desktop' and 'mobile' folders
        if ignore_script_folders:
            for root, dirs, files in os.walk(path, topdown=True):
                dirs[:] = [d for d in dirs if d not in ["desktop", "mobile"]]
                for name in files:
                    # if the file is an image, add it to the list
                    if os.path.splitext(name)[1].lower() in extensions:
                        images.append(os.path.join(root, name))
        # walk through the directory tree
        else:
            for root, dirs, files in os.walk(path):
                for name in files:
                    # if the file is an image, add it to the list
                    if os.path.splitext(name)[1].lower() in extensions:
                        images.append(os.path.join(root, name))
    # if the recursive option is not set, only search the current directory
    else:
        # for each file in the current directory
        for file in os.listdir(path):
            # if the file is an image
            if os.path.splitext(file)[1].lower() in extensions:
                # add the file to the list of images
                images.append(os.path.join(path, file))
    # return the list of images
    return images

# function to get the brightness level of an image
def get_brightness(image):
    # open the image
    img = Image.open(image)
    # get the average brightness level of the image
    # convert the image to grayscale
    # get the histogram of the grayscale image
    # sum the histogram
    # divide by the number of pixels
    brightness = sum(img.convert('L').histogram()) / float(img.size[0] * img.size[1])
    # return the brightness level
    return brightness



# loop over the valid image files, 
# check if they're landscape or portrait,
# put the files in the appropriate folders (desktop for landscape, mobile for portrait)]
def sort_wallpapers_by_orientation(path, recursive):
    # print test
    print("Sorting wallpapers by orientation...")
    # get the list of image files
    images = get_images(path, recursive, ignore_script_folders=True)
    # loop over the image files
    for image in images:
        # open the image
        img = Image.open(image)
        # get the image width and height
        width, height = img.size
        # if the image is landscape
        if width > height:
            # if the desktop folder doesn't exist, create it
            if not os.path.isdir(os.path.join(path, "desktop")):
                os.mkdir(os.path.join(path, "desktop"))
            # move the image to the desktop folder
            if os.rename(image, os.path.join(path, "desktop", os.path.basename(image))):
                # print error
                print("Error: could not move " + os.path.basename(image) + " to desktop folder")
            else:
                # print success
                print("Moved " + os.path.basename(image) + " to desktop folder")
                
            # if the brightness option is set
        # if the image is portrait
        else:
            # if the mobile folder doesn't exist, create it
            if not os.path.isdir(os.path.join(path, "mobile")):
                os.mkdir(os.path.join(path, "mobile"))
            # move the image to the mobile folder
            if os.rename(image, os.path.join(path, "mobile", os.path.basename(image))):
                #print error message
                print("Error: could not move " + os.path.basename(image) + " to mobile folder")
            else:
                # print success message
                print("Moved " + os.path.basename(image) + " to mobile folder")


# function to sort wallpapers by brightness level
def sort_wallpapers_by_brightness(path, recursive):
    # print path
    #print(path)
    # print test
    print("Sorting wallpapers by brightness level...")
    # get the list of image files
    images = get_images(path, recursive, ignore_script_folders=False)
    # print test
    print("Found " + str(len(images)) + " images")
    # loop over the image files
    for image in images:
        # get the brightness level of the image
        brightness = get_brightness(image)
        # if the brightness level is below 128, the image is dark
        if brightness < 128:
            # if the dark folder doesn't exist, create it
            if not os.path.isdir(os.path.join(path, "dark")):
                os.mkdir(os.path.join(path, "dark"))
            # move the image to the dark folder
            if os.rename(image, os.path.join(path, "dark", os.path.basename(image))):
                # print success message
                print("Moved " + os.path.basename(image) + " to dark folder")
            else:
                # print error message
                print("Error: could not move " + os.path.basename(image) + " to dark folder")
        # if the brightness level is above 128, the image is light
        else:
            # if the light folder doesn't exist, create it
            if not os.path.isdir(os.path.join(path, "light")):
                os.mkdir(os.path.join(path, "light"))
            # move the image to the light folder
            if os.rename(image, os.path.join(path, "light", os.path.basename(image))):
                # print success message
                print("Moved " + os.path.basename(image) + " to light folder")
            else:
                # print error message
                print("Error: could not move " + os.path.basename(image) + " to light folder")


# main function
def main():
    # sort wallpapers by orientation
    sort_wallpapers_by_orientation(path, args.recursive)
    # if the brightness option is set
    if args.brightness:
        # if desktop and mobile folders exist,
        # sort wallpapers by brightness level in each folder
        if os.path.isdir(os.path.join(path, "desktop")) and os.path.isdir(os.path.join(path, "mobile")):
            sort_wallpapers_by_brightness(os.path.join(path, "desktop"), args.recursive)
            sort_wallpapers_by_brightness(os.path.join(path, "mobile"), args.recursive)
        # if only the desktop folder exists,
        # sort wallpapers by brightness level in the desktop folder
        elif os.path.isdir(os.path.join(path, "desktop")):
            sort_wallpapers_by_brightness(os.path.join(path, "desktop"), args.recursive)
        # if only the mobile folder exists,
        # sort wallpapers by brightness level in the mobile folder
        elif os.path.isdir(os.path.join(path, "mobile")):
            sort_wallpapers_by_brightness(os.path.join(path, "mobile"), args.recursive)
        # if neither the desktop nor mobile folders exist,
        # sort wallpapers by brightness level in the current folder
        else:
            sort_wallpapers_by_brightness(path, args.recursive)


# call the main function
if __name__ == "__main__":
    main()