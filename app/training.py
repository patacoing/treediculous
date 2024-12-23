from abc import ABC, abstractmethod
import numpy as np
from keras import Sequential
from keras.src.applications.efficientnet import EfficientNetB0
from keras.src.callbacks import History, EarlyStopping
from keras.src.layers import Flatten, Dense, Dropout
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.src.optimizers import Adam


class ITraining(ABC):
    def __init__(self, train_x, train_y, test_x, test_y, num_classes: int):
        self.train_x = np.array(train_x)
        self.train_y = np.array(train_y, dtype=int)
        self.test_x = np.array(test_x)
        self.test_y = np.array(test_y, dtype=int)

    @abstractmethod
    def train(self, epochs: int, batch_size: int) -> tuple[Sequential, History]:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, model: Sequential) -> tuple[float, float]:
        raise NotImplementedError


class Training(ITraining):
    def train(self, epochs: int, batch_size: int, num_classes: int) -> tuple[Sequential, History]:
        size = self.train_x.shape[1]

        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
        train_generator = datagen.flow(self.train_x, self.train_y, batch_size=batch_size)

        base_model = EfficientNetB0(include_top=False, weights='imagenet', input_shape=(size, size, 3))
        base_model.trainable = False

        model = Sequential([
            base_model,
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])

        model.summary()

        earlystopping = EarlyStopping(
            monitor="val_loss",
            mode="min",
            patience=10,
            restore_best_weights=True
        )

        optimizer = Adam(learning_rate=1e-5)

        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=["accuracy"])
        history = model.fit(
            train_generator,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.test_x, self.test_y),
            callbacks=[earlystopping],
        )

        return model, history

    def evaluate(self, model: Sequential) -> tuple[float, float]:
        return model.evaluate(self.test_x, self.test_y)