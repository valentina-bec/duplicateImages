"""
version 0.1.0
import form npz file
(new) create a list of combinations to avoid double evaluation of the images
compare the imgs_arr by mse
return a list with the imgs to delete

maybe next : --> improved way to compute mse?
"""


import numpy as np
import os
from itertools import combinations


def load_data(root):
    """
    :param root: npzfile made by create_foto_database_array.py
    :return: data
    """
    data = np.load(root,  allow_pickle=True)
    return list(zip(data['label'], data['data']))


def mse(img_a, img_b):
    """
    Function that calculates the mean squared error (mse) between two image matrices
    :param img_a: np.array 26 x 26 grayscaled img
    :param img_b: np.array 26 x 26 grayscaled img to compare
    :return: Mean Squared Error (MSE)
    """
    err = np.sum((img_a.astype("float") - img_b.astype("float")) ** 2)
    err /= float(img_a.shape[0] * img_a.shape[1])
    return err


def check_img_quality(img_a, img_b):
    """
    Check img quality, if img has a duplicate, select the image with lower quality to delet
    """
    size_img_a = os.stat(img_a).st_size
    size_img_b = os.stat(img_b).st_size
    if size_img_a > size_img_b:
        return img_b
    elif size_img_a < size_img_b:
        return img_a
    else:
        return str('same quality')


def set_combinations(li):
    """
    :param li: list of files
    :return: list of tuples : possible combination to pairwise comparision n!/((n-m!)*n!)
    """
    label = [li[i][0] for i in range(len(li))]
    comb = list(combinations(label, 2))
    return comb


def compare_comb(li):
    # prepare list:
    list_images_to_delet = list()

    # set the combination to compare
    comb = set_combinations(li)
    total = len(comb)
    # convert list to dic to easy get to the array
    d = dict(li)

    count = 0
    # extract the combination
    for item in comb:
        # check if files exists
        count += 1
        # print('{:0.2%} von {}'.format(count/total, total))
        if os.path.isfile(item[0]) and os.path.isfile(item[1]):
            # print('comparing: {} with {}.'.format(item[0], item[1]))

            # calculate MSE: mean squared error
            error = mse(d[item[0]], d[item[1]])
            # in case of similarity (Threshold: 10)
            if error < 10:
                # select the image with lower quality
                img_lower_quality = check_img_quality(item[0], item[1])

                # append in the list
                list_images_to_delet.append((item[0], item[1], img_lower_quality))
        count += 1
    return list_images_to_delet


# helper functions
def list_to_csv(li):
    np.savetxt("repeated_images.csv",
               li,
               delimiter=", ",
               fmt='% s')
    pass


def print_data(data):
    # pass the data to a list
    li = list(zip(data['label'], data['data']))

    # check the files to compare
    for item in data['label']:
        print(item)
    pass

def main():

    npzfile = r'/Users/valentina/PycharmProjects/duplicateImages/output_all.npz'
    data = load_data(npzfile)
    # check the data
    # print_data(data)

    # list of img to delet
    list_img_to_delet = compare_comb(data)
    print(list_img_to_delet)

    # save the list to csv
    list_to_csv(list_img_to_delet)


main()
