import datetime

import keras
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from pathlib import Path

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, SeparableConv2D, MaxPooling2D
from keras.callbacks import TensorBoard
from pathlib import Path
import joblib
from keras.utils import to_categorical


RUN_NAME = "eric1" + datetime.datetime.now().strftime("_%H_%M")


def build_inhabited_model():
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.15))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.15))
    model.add(Dense(10, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    return model



(x_train_non_normalized, y_train), (x_test, y_test) = cifar10.load_data()

# Load data set
x_train = joblib.load("x_train.dat")

y_train_inhabited_encoded = keras.utils.to_categorical(y_train, 10)
y_test_encoded = keras.utils.to_categorical(y_test, 10)


# Inhabited model
inhabited_model = build_inhabited_model()
inhabited_model.fit(
    x_train,
    y_train_inhabited_encoded,
    epochs=30,
    validation_split=0.01,
    shuffle=True,
    verbose=2,
    callbacks=[
        TensorBoard(log_dir=f'./logs/inhabited/inhabited_{RUN_NAME}', histogram_freq=0, write_graph=True, write_images=True)
    ]
)

# Save results
inhabited_model_structure = inhabited_model.to_json()
f = Path("models") / "inhabited_model_structure.json"
f.write_text(inhabited_model_structure)
inhabited_model.save_weights("models/inhabited_model_weights.h5")