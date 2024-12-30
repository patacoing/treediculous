from abc import ABC, abstractmethod
import numpy as np
from keras import Sequential
from keras.src.applications.efficientnet import EfficientNetB0
from imblearn.over_sampling import RandomOverSampler
from keras.src.applications.vgg16 import VGG16
from keras.src.callbacks import History, EarlyStopping
from keras.src.layers import Flatten, Dense, Dropout, Activation, InputLayer, Conv2D, MaxPooling2D, BatchNormalization
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.src.losses import BinaryCrossentropy, SparseCategoricalCrossentropy
from keras.src.optimizers import Adam, SGD
from keras.src.utils import to_categorical


class ITraining(ABC):
    def __init__(self, train_x, train_y, test_x, test_y, num_classes: int):
        self.train_x = np.array(train_x)
        self.train_y = to_categorical(np.array(train_y, dtype=int), num_classes=num_classes)
        self.test_x = np.array(test_x)
        self.test_y = to_categorical(np.array(test_y, dtype=int), num_classes=num_classes)

    @abstractmethod
    def train(self, epochs: int, batch_size: int) -> tuple[Sequential, History]:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, model: Sequential) -> tuple[float, float]:
        raise NotImplementedError


class Training(ITraining):
    def train(self, epochs: int, batch_size: int, num_classes: int) -> tuple[Sequential, History]:
        size = self.train_x.shape[1]

        oversampler = RandomOverSampler(sampling_strategy="minority")
        self.train_x, self.train_y = oversampler.fit_resample(self.train_x.reshape(-1, size * size * 3), self.train_y)
        self.train_x = self.train_x.reshape(-1, size, size, 3)
        self.train_y = to_categorical(self.train_y, num_classes=num_classes)

        datagen = ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.2,
            height_shift_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
        train_generator = datagen.flow(self.train_x, self.train_y, batch_size=batch_size)

        base_model = VGG16(include_top=False, weights='imagenet', input_shape=(size, size, 3))
        base_model.trainable = False


        model = Sequential([
            # base_model,
            InputLayer(shape=(224, 224, 3)),
            Conv2D(16, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(32, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            BatchNormalization(),
            Conv2D(64, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(128, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(256, kernel_size=(3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            BatchNormalization(),

            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(64, activation='relu'),
            Dropout(0.5),
            # Dropout(0.5),
            Dense(num_classes, activation='softmax'),
        ])

        model.summary()

        print(self.train_x.shape)
        print(self.train_y.shape)
        print(self.test_x.shape)
        print(self.test_y.shape)

        earlystopping = EarlyStopping(
            monitor="val_loss",
            mode="min",
            patience=5,
            restore_best_weights=True
        )

        optimizer = Adam(learning_rate=0.001)

        model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
        history = model.fit(
            # train_generator,
            self.train_x,
            self.train_y,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.test_x, self.test_y),
            # callbacks=[earlystopping],
            verbose=1
        )

        return model, history

    def evaluate(self, model: Sequential) -> tuple[float, float]:
        return model.evaluate(self.test_x, self.test_y)