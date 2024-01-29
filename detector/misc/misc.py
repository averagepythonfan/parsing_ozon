from typing import List
import aiohttp
from PIL.Image import Image, open
from io import BytesIO
from detector.config import TOKEN


async def get_pic(url: str) -> Image:
    """Download pic and return it as PIL's `Image` instance."""

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return open(BytesIO(await response.content.read()))


async def send_to_user(user_id: int, pics: List[dict]):

    URL = f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup"

    params = {
        "chat_id": user_id,
        "media": pics
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=URL, json=params) as response:
            if response.status == 200:
                return True
