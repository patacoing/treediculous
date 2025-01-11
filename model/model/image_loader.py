import json
import os
import shutil
from abc import abstractmethod, ABC
from typing import Callable
import cv2
import numpy as np


class ILoader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, file_path: str):
        raise NotImplementedError


class OpenCvLoader:
    @classmethod
    def load(cls, file_path: str) -> np.array:
        return cv2.imread(file_path)


def is_file(file_path: str) -> bool:
    return os.path.isfile(file_path) and ".DS_Store" not in file_path

def list_files(path: str) -> list[str]:
    return os.listdir(path)


class IImageLoader(ABC):
    def __init__(
        self,
        path: str,
        loader: ILoader = OpenCvLoader(),
        is_file: Callable[[str], bool] = is_file,
        list_files: Callable[[str], list[str]] = list_files
    ):
        self.path = path
        self.images = []
        self.loader = loader
        self.is_file = is_file
        self.list_files = list_files

    @abstractmethod
    def load(self) -> list[np.array]:
        raise NotImplementedError

    @abstractmethod
    def rename(self, destination_path: str):
        raise NotImplementedError

    def get_filenames(self) -> list[str]:
        return list(filter(lambda filename: self.is_file(f"{self.path}/{filename}"), self.list_files(self.path)))


class ImageLoader(IImageLoader):
    def load(self) -> list[tuple[np.array, str]]:

        filenames = self.get_filenames()
        images = [self.loader.load(f"{self.path}/{filename}") for filename in filenames]

        return images, filenames

    def rename(self, destination_path: str):
        filenames = self.get_filenames()
        for i, filename in enumerate(filenames):
            shutil.copy(f"{self.path}/{filename}", f"{destination_path}/{i+1}.jpg")


def load_labels_from_txt(path: str) -> list[str]:
    return list(map(lambda line: line.strip(), open(path, "r").readlines()))

def load_labels_from_annotation_file(path: str, filenames: list[str]) -> list[str]:
    labels_found = {"-".join(entry["file_upload"].split("-")[1:]): entry["annotations"][0]["result"][0]["value"]["choices"][0] for entry in json.load(open(path, "r"))}

    return list(map(lambda filename: labels_found[filename], filenames))
