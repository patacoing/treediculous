from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image
from fastapi import APIRouter, UploadFile, Depends

from model.app.model import Model
from api.app.schemas.response import ResponseSchemas, Classification


router = APIRouter()

model = Model(["ugly", "nice"])
model_path = Path(__file__).resolve().parent.parent / "model" / "treediculous.keras"
if model_path.exists():
    model.load(model_path)
else:
    print("Model not found")

def get_model() -> Model:
    return model

def get_labels() -> list[str]:
    return model.labels


@router.post("/treediculous")
async def infer(
    image: UploadFile,
    model: Model = Depends(get_model),
) -> ResponseSchemas:
    file = await image.read()
    image_as_array = np.array(Image.open(BytesIO(file)))

    prediction, label = model.predict(image_as_array)
    label = Classification(label)

    return ResponseSchemas(
        classname=label,
        probability=prediction,
    )