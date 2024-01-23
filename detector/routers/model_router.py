from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
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
