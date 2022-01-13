"""
version 0.0.1
npz file from create_foto_database_array
load data and check for duplicates by MSE
"""


import numpy as np
import os


def load_data(root):
     return np.load(root,  allow_pickle=True)

def mse(imageA, imageB):
    """
    Function that calculates the mean squared error (mse) between two image matrices
    :param imageA: np.array 26 x 26 grayscaled img
    :param imageB: np.array 26 x 26 grayscaled img to compare
    :return: Mean Squared Error (MSE)
    """
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def check_img_quality(imgA, imgB):
    """
    Check img quality, if img has a duplicate, select the image with lower quality to delet
    """
    size_imgA = os.stat(imgA).st_size
    size_imgB = os.stat(imgB).st_size
    if size_imgA > size_imgB:
        return imgB
    elif size_imgA < size_imgB:
        return imgA
    else:
        return str('same quality')

def compare_images (l):
    """
    select from the list the both imgs to compare
    """
    count = 1
    total_img_to_compare = len(l)
    list_images_to_delet = list()
    for item in l:
        # setting imgA
        rootA, img_matrixA = item[0], item[1]

        print ('looking for doubles {} von {} by file: {}'.format(count, total_img_to_compare, rootA))
        #set imgB
        for item in l:
            rootB, img_matrixB = item[0], item[1]
            if rootA == rootB:
                # do not check the same file
                pass
            else:
                # compare img_matrix
                error = mse(img_matrixA, img_matrixB)
                # in case of similarity (Threshold: 200), select the image with lower quality
                if error < 10:  #threshold 200 do not diferentiate low key (low quality) imgs
                    img_lower_quality = check_img_quality(rootA, rootB)
                    list_images_to_delet.append((rootA, rootB, img_lower_quality))

        count +=1
    return list_images_to_delet

# helper funcions
def list_to_csv(list):
    np.savetxt("repeated_images.csv",
               list,
               delimiter=", ",
               fmt ='% s')
    pass

def print_data(data):
    li = list(zip(data['label'], data['data']))
    for item in data['label']:
        print(item)
    pass

def main():

    npzfile = r'/Users/valentina/PycharmProjects/duplicateImages/output_all.npz'
    data = load_data(npzfile)
    #check the data
    #print_data(data)
    li = list(zip(data['label'], data['data']))
    list_img_to_delet = compare_images(li)
    list_to_csv(list_img_to_delet)

main()