import argparse
from pathlib import Path

from app.model import Model


parser = argparse.ArgumentParser("training")
parser.add_argument("--train_images_input", type=str)
parser.add_argument("--train_labels_input", type=str)
parser.add_argument("--test_images_input", type=str)
parser.add_argument("--test_labels_input", type=str)
parser.add_argument("--model_output", type=str)

args = parser.parse_args()
train_images_input = args.train_images_input
train_labels_input = args.train_labels_input
test_images_input = args.test_images_input
test_labels_input = args.test_labels_input
model_output = args.model_output

mapping = {
    "ugly": 0,
    "nice": 1
}

model = Model(list(mapping.keys()))

NB_EPOCHS = 100
NB_BATCH_SIZE = 32
MODEL_NAME = "treediculous"

model.train(
    Path(f"{train_labels_input}/labels.txt"),
    Path(train_images_input),
    Path(f"{test_labels_input}/labels.txt"),
    Path(test_images_input),
    nb_batch_size=NB_BATCH_SIZE,
    nb_epochs=NB_EPOCHS,
)

Path(model_output).mkdir(parents=True, exist_ok=True)

model.save(f"{model_output}/{MODEL_NAME}.keras")