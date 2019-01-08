import concurrent
from pathlib import Path

from keras.applications import vgg16
import joblib
from keras.datasets import cifar10
import scipy.misc
import numpy as np
from keras_preprocessing.image import ImageDataGenerator
from scipy.misc import imresize
import os


# Load data set
(x_augmented, y_train), (x_test, y_test) = cifar10.load_data()

UPSCALED_FILENAME = Path("upscaled_x_images.dat")

if not UPSCALED_FILENAME.exists():


    l = []



    # upscale to 64x64
    upper_limit = x_augmented.shape[0]
    for i in range(upper_limit):
        temp = x_augmented[i, :, :, :].copy()
        temp = imresize(temp, (temp.shape[0]*2, temp.shape[1]*2, 3))
        l.append(temp)

        if i % 10 == 0:
            print(f"{i} of {upper_limit}")

    x_augmented = np.array(l)

    joblib.dump(x_augmented, UPSCALED_FILENAME)
else:
    x_augmented = joblib.load(UPSCALED_FILENAME)
#scipy.misc.imresize

print("Preprocess input")

#with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:

feature_extractor = vgg16.VGG16(weights='imagenet', include_top=False, input_shape=(64, 64, 3))

x_train = vgg16.preprocess_input(x_augmented)


print("Extract features from images")
features_x = feature_extractor.predict(x_train, batch_size=8)

    # Dump results from this batch to disk
print(f"features.dat")
joblib.dump(features_x, f"x_train.dat")