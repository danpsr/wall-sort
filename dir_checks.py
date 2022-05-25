import os
from os.path import exists, isfile, join


def init_dir_checks(target_path):

    # bad_paths = ["/dev"]

    # for badf in bad_paths:
    if target_path.startswith("/dev"):
        print("Invalid directory.")
        return False

    if not os.path.isdir(target_path):
        print("Given directory doesn't exist!")
        return False
    elif target_path.strip() == "/":
        print("Given directory is the root of the drive; not using that.")
        return False

    return True


def get_dir_img_list(target_path):

    target_files = []

    # listing directories
    for file in os.listdir(target_path):
        # cares only for the actual files, ignores subdirectories
        # uses join() to join the target path and the filename so the path is complete and valid
        if isfile(join(target_path, file)):
            # prints file name only if it's one of the supported image formats
            # converts everything to lowercase first to avoid dumb shit
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                target_files.append(file)

    return target_files


# removes the ./ characters, if present, because they fuck with the way i handle paths in this thing
# startswith() allows you to supply a tuple with a list of strings to test with
def clean_path(path):
    first_valid_char = re.search("[a-zA-Z0-9]", path).start()

    if path[first_valid_char - 1] == ".":
        path = path[first_valid_char - 1 :]
    else:
        path = path[first_valid_char:]

    return path
