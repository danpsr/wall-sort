# script that sorts wallpapers into folders depending on
# whether they're desktop wallpapers (landscape orientation) or mobile wallpapers (portrait orientation)

# argument parser to get the path to the wallpapers folder
# if no path is given, the current directory is used
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to wallpapers folder", nargs='?', default='.') 
# add recursive option
parser.add_argument("-r", "--recursive", help="recursively sort wallpapers in subfolders", action="store_true")
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


# get the list of files in the wallpapers folder
# search recursively only if the user has passed the -r (--recursive) flag
# but do not search the 'desktop' and 'mobile' folders
files = []
if args.recursive:
    for root, dirs, filenames in os.walk(path):
        if 'desktop' in dirs:
            dirs.remove('desktop')
        if 'mobile' in dirs:
            dirs.remove('mobile')
        for filename in filenames:
            files.append(os.path.join(root, filename))
else:
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

# get only the image files from the list of files
image_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]



# loop over the valid image files, 
# check if they're landscape or portrait,
# put the files in the appropriate folders (desktop for landscape, mobile for portrait)
for file in image_files:
    image = Image.open(path + '/' + file)
    width, height = image.size
    if width > height:
        if not os.path.exists(path + '/desktop'):
            os.makedirs(path + '/desktop')
        # print a success message if the file was successfully sorted
        # also print the old path and the new path, but omit the full path to the wallpapers folder
        if os.rename(path + '/' + file, path + '/desktop/' + file):
            print("Success: " + file + " -> " + 'desktop/' + file)
    else:
        if not os.path.exists(path + '/mobile'):
            os.makedirs(path + '/mobile')
        # print a success message if the file was successfully sorted
        # also print the old path and the new path, but omit the full path to the wallpapers folder
        if os.rename(path + '/' + file, path + '/mobile/' + file):
            print("Success: " + file + " -> " + 'mobile/' + file)
