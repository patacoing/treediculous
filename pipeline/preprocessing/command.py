print("coucou")
import argparse
from PIL import Image

print("coucou")

from model.image_loader import ImageLoader
from model.preprocessing import OpenCvPreprocessing, IPreprocessing

print("coucou")


parser = argparse.ArgumentParser("preprocess")
parser.add_argument("--images_input", type=str)
parser.add_argument("--images_output", type=str)

args = parser.parse_args()
images_input = args.images_input
images_output = args.images_output

print("loading images")
image_loader = ImageLoader(images_input)
images, filenames = image_loader.load()
print("images loaded")

print("preprocessing images")
open_cv_preprocessing = OpenCvPreprocessing(images)
images = open_cv_preprocessing.preprocess()
print("images preprocessed")

print("saving images")
images = (images * IPreprocessing.NORMALIZATION).astype("uint8")
for image, filename in zip(images, filenames):
    im = Image.fromarray(image)
    im.save(f"{images_output}/{filename}")
print("images saved")