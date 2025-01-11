import numpy as np
from keras import Sequential
from keras.src.callbacks import History
from keras.src.saving import load_model

from model.image_loader import ImageLoader, load_labels_from_txt
from model.preprocessing import OpenCvPreprocessing
from model.training import Training


class Model:
    def __init__(self, labels: list[str]):
        self.model = Sequential()
        self.labels = labels

    def load(self, path: str):
        self.model = load_model(path)

    def save(self, path: str):
        self.model.save(path)

    def train(
        self,
        train_annotations_path: str,
        train_path: str,
        test_annotations_path: str,
        test_path: str,
        nb_epochs: int=10,
        nb_batch_size: int=32
    ) -> History:
        train_labels = load_labels_from_txt(train_annotations_path)
        test_labels = load_labels_from_txt(test_annotations_path)

        image_loader = ImageLoader(train_path)
        train_images, filenames = image_loader.load()

        image_loader = ImageLoader(test_path)
        test_images, filenames = image_loader.load()

        open_cv_preprocessing = OpenCvPreprocessing(np.array(train_images))
        open_cv_preprocessing.normalize()
        train_images = open_cv_preprocessing.images
        open_cv_preprocessing = OpenCvPreprocessing(np.array(test_images))
        open_cv_preprocessing.normalize()
        test_images = open_cv_preprocessing.images

        train_x, train_y, test_x, test_y = train_images, train_labels, test_images, test_labels

        training = Training(train_x, train_y, test_x, test_y, 1)
        model, history = training.train(epochs=nb_epochs, batch_size=nb_batch_size, num_classes=1)

        self.model = model

        return history

    @staticmethod
    def _preprocess_image(image: np.array) -> np.array:
        preprocessing = OpenCvPreprocessing([image])
        image = preprocessing.preprocess()[0]
        return image

    def predict(self, image: np.array, verbose: int = 0) -> tuple[list[float], str]:
        image_preprocessed = self._preprocess_image(image)
        prediction = self.model.predict(image_preprocessed.reshape(1, 224, 224, 3), verbose=verbose)[0][0]

        return prediction, self.labels[int(prediction > 0.5)]