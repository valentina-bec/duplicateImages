
"""
need better algorithm to compare the matrices.
I'm not convinced it is the best way, but it works
and image rotation has not been implemented yet
"""

import numpy as np
import cv2
import os
import imghdr
import pandas as pd

from tkinter.filedialog import askdirectory


def create_imgs_matrix(directory):
    """
    look for images in subdirectories
    :return: list with root , filename
    """
    list_of_images = list()
    # walk into the dirs and subdirs
    for root, dirs, files in os.walk(directory):
        for filename in files:
            img_file = '{}/{}'.format(root, filename)
            # pick only images file
            if imghdr.what(img_file):
                # decode to a matrix
                img_matrix = img_to_matrix(img_file)
                # put in a list
                list_of_images.append((root, filename, img_matrix))
    return list_of_images

def img_to_matrix(img):
    """
    :param img: path of image file to convert
    :return: imagefile as np.array
    """
    #decode the image and create the matrix
    img_matrix = cv2.imdecode(np.fromfile(img, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # resize the image based on the given compression value
    px_size = 50 # default
    if type(img) == np.ndarray:
        img_matrix = cv2.resize(img, dsize=(px_size, px_size), interpolation=cv2.INTER_CUBIC)
        print('{} passed to np.array'.format(img))
    return img_matrix



def mse(imageA, imageB):
    """
    Function that calculates the mean squared error (mse) between two image matrices
    :param imageA:
    :param imageB:
    :return:
    """
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def rotate_img(image):
    """
    Function for rotating an image matrix by a 90 degree angle
    :param image:
    :return:
    """
    image = np.rot90(image, k=1, axes=(0, 1))
    return image

def check_img_quality(imageA, imageB):
    """
    Function for checking the quality of compared images
    """
    size_imgA = os.stat(imageA).st_size
    size_imgB = os.stat(imageB).st_size
    if size_imgA > size_imgB:
        return imageB
    elif size_imgA < size_imgB:
        return imageA
    else: return str('same quality')

def compare_images (list_of_images):
    list_images_to_delet = list()
    for item in list_of_images:
        # settings of img A
        rootA = item[0]
        filenameA = '{}/{}'.format(rootA, item[1])
        img_matrixA = item[2]
        print('looking for doubles of {}.....'.format(filenameA))
        for item in list_of_images:
            #settings of img B
            rootB = item[0]
            filenameB = '{}/{}'.format(rootB, item[1])
            img_matrixB = item[2]
            if filenameA == filenameB:
                #do not check the same file
                pass
            else:
                print ('...comparing {} and {}.'.format(filenameA, filenameB))
                # compare img_matrix
                error = mse(img_matrixA, img_matrixB)
                # in case of similarity (Threshold: 200), select the image with lower quality
                if error < 200:
                    img_lower_quality = check_img_quality(filenameA, filenameB)
                    list_images_to_delet.append((filenameA, filenameB, img_lower_quality))
    return list_images_to_delet

def list_to_csv(list):
    np.savetxt("repeated_images.csv",
               list,
               delimiter=", ",
               fmt ='% s')
    pass

def main(src):
    # select the files to review
    list_of_images = create_imgs_matrix(src) # with root and file
    list_of_images_to_delete = compare_images(list_of_images)
    list_to_csv(list_of_images_to_delete)
    pass

src = askdirectory()
main(src)