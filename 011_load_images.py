import random
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from config import *

IMG_CHANNELS = 3

# Read images from Original path (the folder given by Luppi)
tot_num = len(os.listdir(AllImages))  # 252
# 252-273

# Fix number of test images 58: 2 additional images are insterted manually
# because we need them in the test (see next jupyter cell)
NumberTest = 58
test_names = []
UpperLimit = tot_num

random.seed(99)
# collect random number to select test set
# until 58 names are completed

while len(test_names) < NumberTest:
    x = random.randint(0, UpperLimit)
    if x not in test_names:
        test_names.append(x)
    else:
        continue

test_names.append(254)  # maccheroni images needed in the test
test_names.append(81)  # yellow strip artifact
test_names.sort()

# Our images name are 0.tiff, 1.tiff and so on
# the format is .tiff and no more .TIF as the firts experiment run
# I failed to save in .TIF format when reading from original dataset
# If we want to fix this, we need to change 010_load_file_join_all_images
images_name = os.listdir(AllImages)
# select only the number
images_name = [int(x.split('.')[0]) for x in images_name]
# sort the images
images_name.sort()
# restore the original name
images_name = [str(x) + '.tiff' for x in images_name]

# %%

# Split images it train_val and test folder
# during the reading the images if the binary mask has more than two values:
# 0 for black and 255 for white this could be related to spurious saving effect from
# GIMP and imageJ software (interpolation???). We need to reset only 0 and 255 value
# We did in the #############Processing############### section below
for ix, im_name in enumerate(images_name):

    #############Processing###############

    print(im_name)
    img_x = cv2.imread(str(AllImages) + im_name)
    img_x = cv2.cvtColor(img_x, cv2.COLOR_BGR2RGB)
    img_y = cv2.imread(str(AllMasks) + im_name)
    img_y = cv2.cvtColor(img_y, cv2.COLOR_BGR2RGB)[:, :, 0:1]

    #############Processing###############
    if len(np.unique(img_y)) > 2:
        print(' restoring {}'.format(im_name))

        ret, img_y = cv2.threshold(img_y, 75, 255, cv2.THRESH_BINARY)

    img_y = img_y.astype(bool)
    img_y = img_y.astype(np.uint8) * 255

    #############Saving in new folder###############

    if int(im_name.split('.')[0]) in test_names:
        print('test')
        img_dir = TestImages + '{}'.format(im_name)
        mask_dir = TestMasks + '{}'.format(im_name)
        plt.imsave(fname=img_dir, arr=np.squeeze(img_x))
        plt.imsave(fname=mask_dir, arr=np.squeeze(img_y), cmap='gray')

    else:

        img_dir = TrainValImages + '{}'.format(im_name)
        mask_dir = TrainValMasks + '{}'.format(im_name)
        plt.imsave(fname=img_dir, arr=np.squeeze(img_x))
        plt.imsave(fname=mask_dir, arr=np.squeeze(img_y), cmap='gray')

