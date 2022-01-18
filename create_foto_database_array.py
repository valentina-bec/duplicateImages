import os
import imghdr
import numpy as np
import cv2
from tkinter.filedialog import askdirectory

"""
version 0.0.2
preparation of the img_data
 - go through the dirs
 - extract files to check
 - convert img into a np.array
    - resize  26 x 26 
    - grayscale
- save the dataset in npz-file: array and file as label 
 
"""


def select_imgs(src):
    """
    Input the source,
    output: list of img_path to convert.
    """
    # for a dir
    if os.path.isdir(src):
        return list_img_path(src)

    # for a file
    elif os.path.isfile(src) and imghdr.what(src) != 'gif':
        return [src]
    else:
        print("directory or file not accepted, please select an other one!")  # Error Value


def list_img_path(directory):
    """
    input : directory
    return: list of images from subdirectories
    """
    exts = ['jpeg', 'jpg', 'bmp', 'png']
    list_img = list()
    # go through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # select a file
            file_path = os.path.join(root, file)
            # read the ext of file
            img_ext = imghdr.what(file_path)
            # if file is a img
            if img_ext in exts:
                # save to the img_path list
                list_img.append(file_path)
    return list_img


def encode_img_list(l_pfad):
    l_img_array = list()
    for item in l_pfad:
        img_list = encode_img(item)
        img_array = np.array(img_list, dtype=object)
        if img_array.shape == (26, 26):
            l_img_array.append(img_array)

        else:
            print("array size of {} is not ok".format(item))
            l_img_array.append("array size is not ok")

    return l_pfad, l_img_array


def encode_img(img_file):
    if imghdr.what(img_file):
        img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
        # reduce
        px_size = 26
        resize_img = cv2.resize(img, dsize=(px_size, px_size), interpolation=cv2.INTER_CUBIC)
        # convert in grey
        gray_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
        return gray_img
    else:
        print('file cannot be converted into a matrix')


# helper functions
def save_np(destination, data, label):
    np.savez(destination, data=data, label=label)
    pass


def main():
    # select dir or img so convert into array
    dir0 = askdirectory()

    # choose the images, that can be converted into arrays
    l_img_path_roh = select_imgs(dir0)
    print('{} images were found.'.format(len(l_img_path_roh)))

    # convert the imgs into arrays
    l_img_path, l_img_array = encode_img_list(l_img_path_roh)
    print('{} images were converted into an array.'.format(len(l_img_array)))

    # save the database as .npz
    destination = r'/output.npz'
    save_np(destination, l_img_array, l_img_path)
    pass


main()
