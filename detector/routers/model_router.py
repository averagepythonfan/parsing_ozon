from io import BytesIO
from typing import Annotated
from fastapi import APIRouter, Depends, File
from detector.misc import get_pic, send_to_user, user_feedback
from detector.services import ModelService, PymongoService
from detector.dependencies import get_model_service, get_mongo_service
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
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
) -> dict:
    """Accept dict with `user_id` and links of images.
    
    Then send pics with humans to user according to Telegram Bot API."""

    humans = []

    for i, url in enumerate(input.images):
        if i % 10 == 0:
            await user_feedback(
                user_id=input.user_id,
                message=f"проверено {i} из {len(input.images)}, людей {len(humans)}"
            )
        image: Image = await get_pic(url=url)
        if model.one_image(image=image):
            humans.append({
                "type": "photo",
                "media": url
            })
            mongo.add_pic(
                link=url,
                yolo=True,
                article=input.article,
                ozon=input.ozon
            )
        else:
            mongo.add_pic(
                link=url,
                yolo=False,
                article=input.article,
                ozon=input.ozon
            )

        if len(humans) == 10:
            await send_to_user(input.user_id, humans)
            humans = []

    if len(humans) != 0:
        await send_to_user(input.user_id, humans)

    return {"message": "Done!"}


@router.post("/from_file")
async def detect_from_file(
    file: Annotated[bytes, File()],
    model: Annotated[ModelService, Depends(get_model_service)],
):
    """Load file from your computer and get result."""

    pic = Image.open(BytesIO(file))

    return model.from_pic(image=pic)
