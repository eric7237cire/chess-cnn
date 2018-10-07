"""
Training
"""

from __future__ import print_function

import datetime

import joblib
import keras
from keras.callbacks import TensorBoard
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.models import Sequential
from sklearn.model_selection import train_test_split

from config import Config

batch_size = 32
epochs = 10

RUN_NAME = "eric1" + datetime.datetime.now().strftime("_%H_%M")

num_predictions = 20

model_name = 'keras_chess_trained_model.h5'

X = joblib.load(Config.TRAINING_DATA_DIR / "X.dat")
Y = joblib.load(Config.TRAINING_DATA_DIR / "Y.dat")

# CNN networks expect 4th dimension to be channel
# (batch, height, width, channels)
X = X.reshape(list(X.shape) + [1])

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.33, random_state=42)

# The data, split between train and test sets:

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(Config.NUM_CLASSES))
model.add(Activation('softmax'))

# initiate RMSprop optimizer
opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, Config.NUM_CLASSES)
y_test = keras.utils.to_categorical(y_test, Config.NUM_CLASSES)

x_train /= 255
x_test /= 255

print('Fitting model')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test),
          shuffle=True,
          verbose=2,
          validation_split=0.01,
          callbacks=[
              TensorBoard(log_dir=str(Config.TENSOR_BOARD_LOG_DIR / f'chess_pieces/run_{RUN_NAME}'), histogram_freq=0,
                          write_graph=True, write_images=True)
          ]
          )

# Save model and weights
Config.MODELS_DIR.mkdir(exist_ok=True)

model_path = Config.MODELS_DIR / model_name
model.save(str(model_path))
print('Saved trained model at %s ' % model_path)

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
