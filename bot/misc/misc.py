from typing import Optional
import aiohttp
from bson import ObjectId
from bot.config import PARSER, TF_DETECTOR
import os
from pathlib import Path
from PIL.Image import open
from io import BytesIO


async def send_parse_request(user_id: int, article: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{PARSER}:8080/parser/article",
                json={"user_id": user_id, "article": article}
            ) as resp:
                if resp.status != 200:
                    jsoned = await resp.json()
                    print(f"Non 200 status: {jsoned}")
                    return True
    except aiohttp.ClientConnectionError:
        return True


async def send_pic_to_detector(file_path: str) -> Optional[bool]:
    data = aiohttp.FormData()

    pic = open(file_path, "rb")

    data.add_field(
        name="file",
        value=pic,
        filename=file_path,
        content_type="image/jpeg"
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"http://{TF_DETECTOR}:9091/model/from_pic", data=data) as resp:
            if resp.status == 200:
                pic.close()
                return True
            else:
                pic.close()


def save_pic(link: str, obj_id: ObjectId, human: bool):

    path = '/tmp/data/'

    if not os.path.exists(path=path):
        os.mkdir(path=path)
