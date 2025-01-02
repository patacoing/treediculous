from abc import ABC, abstractmethod
import cv2
import numpy as np


class IPreprocessing(ABC):
    NORMALIZATION: int = 255

    @abstractmethod
    def resize(self, size: int=300):
        raise NotImplementedError

    @abstractmethod
    def normalize(self):
        raise NotImplementedError

    def preprocess(self) -> np.array:
        self.resize()
        self.normalize()

        return self.images


class OpenCvPreprocessing(IPreprocessing):
    def __init__(self, images: list[np.array]):
        self.images = images

    def resize(self, size: int=224):
        tmp = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB) for image in self.images]
        self.images = np.array([cv2.resize(image, (size, size)) for image in tmp])

    def normalize(self):
        self.images = self.images / self.NORMALIZATION