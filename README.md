# duplicateImages
finde duplicates by reading images and comparing with MSE:

create_foto_database_array.py:
 - go through the dirs
 - extract files to check
 - convert img into a np.array
    - resize  26 x 26 
    - grayscale
- save the dataset in npz-file: array and file as label 



find_duplicates_mse.py:#

- import npz file
- create a list of combination of images to compare to avoid double check
- compare imgs_array with mse
- return a list with imgs to delete


it could be nice: 

pre-sort the imgs_array to compare them effectively (selection-sort).
comparision with eigenvalues? PCA 

