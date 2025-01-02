from io import BytesIO
import numpy as np
from PIL import Image
from fastapi import APIRouter, UploadFile, Depends

from model.app.model import get_model, Model
from api.app.schemas.response import ResponseSchemas, Classification


router = APIRouter()


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