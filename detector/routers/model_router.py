from io import BytesIO
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException
from detector.misc import get_pic
from detector.services import ModelService
from detector.dependencies import get_model_service
from detector.schemas import InputImages
from PIL import Image


router = APIRouter(
    prefix="/model",
    tags=['Model']
)


@router.post("/detect")
async def detect_person(
    input: InputImages,
    model: Annotated[ModelService, Depends(get_model_service)],
) -> list:
    
    all_images = []

    for url in input.images:
        image: Image = await get_pic(url=url)
        all_images.append(image)

    return model.detect(images=all_images)


@router.post("/from_file")
async def detect_from_file(
    file: Annotated[bytes, File()],
    model: Annotated[ModelService, Depends(get_model_service)],
):
    pic = Image.open(BytesIO(file))

    return model.detect(images=pic)
