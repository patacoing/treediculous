import argparse
from PIL import Image

from app.image_loader import ImageLoader, load_labels_from_annotation_file
from app.splitter import Splitter


parser = argparse.ArgumentParser("splitting")
parser.add_argument("--labels_input", type=str)
parser.add_argument("--images_input", type=str)
parser.add_argument("--train_labels_output", type=str)
parser.add_argument("--train_images_output", type=str)
parser.add_argument("--test_labels_output", type=str)
parser.add_argument("--test_images_output", type=str)

args = parser.parse_args()
images_input = args.images_input
labels_input = args.labels_input
train_labels_output = args.train_labels_output
train_images_output = args.train_images_output
test_labels_output = args.test_labels_output
test_images_output = args.test_images_output

print("loading images")
image_loader = ImageLoader(images_input)
images, filenames = image_loader.load()
print("images loaded")

print("loading labels")
mapping = {
    "ugly": 0,
    "nice": 1
}
labels = load_labels_from_annotation_file(f"{labels_input}/project-1-at-2024-12-23-22-37-9b90e95a.json", filenames)
print("labels loaded")

print("splitting data")
splitter = Splitter(images, list(map(lambda label: mapping[label], labels)))
splitter.split(0.8)

train_images = splitter.train_x
train_labels = splitter.train_y
test_images = splitter.test_x
test_labels = splitter.test_y
print("data splitted")

print("saving images")
for index, image in enumerate(train_images):
    im = Image.fromarray(image)
    im.save(f"{train_images_output}/{index}.jpg")

for index, image in enumerate(test_images):
    im = Image.fromarray(image)
    im.save(f"{test_images_output}/{index}.jpg")
print("images saved")

print("saving labels")
with open(f"{train_labels_output}/labels.txt", "w") as file:
    for label in train_labels:
        file.write(f"{label}\n")

with open(f"{test_labels_output}/labels.txt", "w") as file:
    for label in test_labels:
        file.write(f"{label}\n")
print("labels saved")