import aiohttp
from PIL.Image import Image, open
from io import BytesIO


async def get_pic(url: str) -> Image:
    """Download pic and return it as PIL's `Image` instance."""

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return open(BytesIO(await response.content.read()))
