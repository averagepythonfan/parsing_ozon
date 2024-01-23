import asyncio
import aiohttp
from PIL import Image
from io import BytesIO


async def download_pic(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return Image.open(BytesIO(await response.content.read()))



URL = "https://sun9-12.userapi.com/impf/UDomoKXxVYmyMhNzTrYq9oRftOlI63OQlAEOKg/U7PX-aOvLxI.jpg?size=1950x1300&quality=95&sign=25c368ea8c42a6bbd8e03a8c99456cda&type=album"


asyncio.run(download_pic(url=URL))
