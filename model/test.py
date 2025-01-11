from pathlib import Path

from PIL import Image
from matplotlib import pyplot as plt

from model.image_loader import ImageLoader, load_labels_from_annotation_file
from model.model import Model
from model.preprocessing import OpenCvPreprocessing, IPreprocessing
from model.splitter import Splitter

image_Loader = ImageLoader(path="data/")
image_Loader.rename("data_renamed/")
exit()



images, filenames = image_Loader.load()

preprocessing = OpenCvPreprocessing(images)
images = preprocessing.preprocess()

labels = load_labels_from_annotation_file("project-1-at-2024-12-28-13-38-0d340661.json", filenames)

# images = (images * IPreprocessing.NORMALIZATION).astype("uint8")
# for image, filename in zip(images, filenames):
#     im = Image.fromarray(image)
#     im.save(f"test/{filename}")

mapping = {
    "ugly": 0,
    "nice": 1
}


splitter = Splitter(images, list(map(lambda label: mapping[label], labels)))
splitter.split(0.8)

train_x, test_x, train_y, test_y = splitter.train_x, splitter.test_x, splitter.train_y, splitter.test_y

print(f"{len(train_x)=}")
print(f"{len(train_y)=}")
print(f"{len(test_x)=}")
print(f"{len(test_y)=}")

train_x = (train_x * IPreprocessing.NORMALIZATION).astype("uint8")
test_x = (test_x * IPreprocessing.NORMALIZATION).astype("uint8")


train_labels_input = "test/train_labels"
train_images_input = "test/train_images"
test_labels_input = "test/test_labels"
test_images_input = "test/test_images"

print("saving images")
for index, image in enumerate(train_x):
    im = Image.fromarray(image)
    im.save(f"{train_images_input}/{index}.jpg")

for index, image in enumerate(test_x):
    im = Image.fromarray(image)
    im.save(f"{test_images_input}/{index}.jpg")
print("images saved")

print("saving labels")
with open(f"{train_labels_input}/labels.txt", "w") as file:
    for label in train_y:
        file.write(f"{label}\n")

with open(f"{test_labels_input}/labels.txt", "w") as file:
    for label in test_y:
        file.write(f"{label}\n")
print("labels saved")

model = Model(mapping.keys())
nb_epochs = 100

history = model.train(
    Path(f"{train_labels_input}/labels.txt"),
    Path(train_images_input),
    Path(f"{test_labels_input}/labels.txt"),
    Path(test_images_input),
    nb_batch_size=32,
    nb_epochs=nb_epochs,
)

plt.plot(range(len(history.history["loss"])), history.history['loss'], color = 'blue', label="loss")
plt.plot(range(len(history.history["val_loss"])), history.history['val_loss'], color = 'green', label="val_loss")
plt.xlabel("Epoch")
plt.ylabel("loss / Val loss")
plt.legend()
plt.savefig("graph.png")
