
"""
need better algorithm to compare the matrices.
I'm not convinced it is the best way, but it works
and image rotation has not been implemented yet

-->

Mean Squared Error (MSE)
Root Mean Squared Error (RMSE)
Peak Signal-to-Noise Ratio (PSNR)
Structural Similarity Index (SSIM)
Universal Quality Image Index (UQI)
Multi-scale Structural Similarity Index (MS-SSIM)
Erreur Relative Globale Adimensionnelle de Synthèse (ERGAS)
Spatial Correlation Coefficient (SCC)
Relative Average Spectral Error (RASE)
Spectral Angle Mapper (SAM)
Visual Information Fidelity (VIF)
"""

import cv2
import os
import imghdr

import numpy as np


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
            if os.path.getsize(img_file) ==0:
                list_of_images.append((root, filename, 'no bytes'))
                pass
            else:
                if imghdr.what(img_file) and imghdr.what(img_file) != 'gif': # remove gif
                    #print (imghdr.what(img_file))
                    # decode to a matrix
                    #img_matrix = img_to_matrix(img_file)
                    img_matrix = img_to_tensor(img_file) # test simplified
                    # put in a list
                    list_of_images.append((root, filename, img_matrix))

    return list_of_images

def img_to_tensor(img_file):
    """

    """
    print ("...decoding img :", img_file)
    if imghdr.what(img_file):
        #read the image
        img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
        #reduce
        px_size = 50
        return cv2.resize(img, dsize=(px_size, px_size), interpolation=cv2.INTER_CUBIC)
    else: print ("image cannnot be converted") # better with Error Value... to implement


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

def select_img_for_comparison(list):
    # settings of img A

    pass

def compare_images (list_of_images):

    """
    setting A und setting B in loop is not to optimal.
    it should be improved.
    """
    list_images_to_delet = list()
    for item in list_of_images:
        # settings of img A
        rootA, filenameA, img_matrixA = item[0], '{}/{}'.format(item[0], item[1]), item[2]
        if img_matrixA == 'no bytes':
            # list
            list_images_to_delet.append((filenameA, '...', 'no bytes'))
            # and remove from the list:
            list_of_images.remove(item)
            print (item, r'\n', '....was removed')
        else:
            print('looking for doubles of {}.....'.format(filenameA))
            for item in list_of_images:
                #settings of img B
                rootB, filenameB, img_matrixB = item[0], '{}/{}'.format(item[0], item[1]), item[2]

                if filenameA == filenameB or img_matrixB == 'no bytes' :
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