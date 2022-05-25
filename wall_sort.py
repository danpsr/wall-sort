from PIL import Image
import os, sys, argparse, shutil, logging
from os.path import isfile, join, isabs
from dir_checks import *

# testing argparse
parser = argparse.ArgumentParser(
    prog="wallpaper-sorter.py",
    description="Sorts wallpapers from target_folder into separate phone and pc wallpaper folders.",
)

parser.add_argument("target_path", help="Specifies target directory")
parser.add_argument(
    "-v",
    "--verbose",
    action="store_const",
    dest="verbose",
    const=True,
    help="Show program messages",
)
args = parser.parse_args()

if not init_dir_checks(args.target_path):
    exit(1)

if args.target_path[-1] != "/":
    args.target_path = args.target_path + "/"


def sort_papes():

    # gets list of valid images in the target directory
    target_files = get_dir_img_list(args.target_path)

    # if there are no valid images, exit
    if len(target_files) == 0:
        print("No wallpapers here! Exiting.")
        exit(1)

    phone_wp_dir = join(args.target_path, "phone_wallpapers")
    pc_wp_dir = join(args.target_path, "pc_wallpapers")

    if not os.path.isdir(phone_wp_dir):
        os.mkdir(phone_wp_dir)
    if not os.path.isdir(pc_wp_dir):
        os.mkdir(pc_wp_dir)

    for file in target_files:
        file_fullpath = join(args.target_path, file)
        wp = Image.open(file_fullpath)
        if wp.height > wp.width:
            # copies the files, if file with the same name already exists in destination, it will be replaced
            if shutil.move(file_fullpath, join(phone_wp_dir, file)):
                if args.verbose == True:
                    print("Moved {} to {}".format(file, join(phone_wp_dir, file)))
        else:
            if shutil.move(file_fullpath, join(pc_wp_dir, file)):
                if args.verbose == True:
                    print("Moved {} to {}".format(file, join(pc_wp_dir, file)))


sort_papes()
