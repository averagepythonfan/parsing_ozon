import asyncio
import re
import random
import aiohttp
from playwright.async_api import async_playwright
from fastapi.exceptions import HTTPException
from parser.config import DETECTOR, TOKEN


class ParserService:

    pl_ctx = async_playwright()
    scroll_down = '''
        const scrollStep = 200; // Размер шага прокрутки (в пикселях)
        const scrollInterval = 100; // Интервал между шагами (в миллисекундах)

        const scrollHeight = document.documentElement.scrollHeight;
        let currentPosition = 0;
        const interval = setInterval(() => {
            window.scrollBy(0, scrollStep);
            currentPosition += scrollStep;

            if (currentPosition >= scrollHeight) {
                clearInterval(interval);
            }
        }, scrollInterval);
    '''
    wc = [f"/wc{i}00/" for i in range(1, 10)]
    tg_feedback_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


    def __init__(self) -> None:
        self.links = dict()


    async def feedback_call(self, message: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.tg_feedback_url, json={"chat_id": self.user_id, "text": message}) as resp:
                if resp.status != 200:
                    print("Сообщение не доставлено")


    async def _new_page(self):
        self._browser = await self.pl.firefox.launch(headless=True)
        self._context = await self._browser.new_context()
        return await self._context.new_page()


    async def _parse_html(self, page):
        """Find all links by regexp."""

        a_handle = await page.evaluate_handle("document.body")
        result_handle = await page.evaluate_handle("body => body.innerHTML", a_handle)
        html = str(await result_handle.json_value())
        await result_handle.dispose()

        find = "https://ir.ozone.ru/s3/rp-photo-[0-9]/wc[0-9]00/.*?jpeg"
        vid = "https://ir.ozone.ru/s3/video-[0-9]/.*?.jpg"
        pics = re.findall(find, html)
        thumbnails = re.findall(vid, html)
        
        for el in pics:
            hashed_pic = el[40:-5]
            if self.links.get(hashed_pic):
                continue
            else:
                self.links[hashed_pic] = el
        
        for el in thumbnails:
            hashed_thumb = el[32:-22]
            if self.links.get(hashed_thumb):
                continue
            else:
                self.links[hashed_thumb] = el


    async def parse(self, article: int, user_id: int):
        self.url = "https://www.ozon.ru/product/" + str(article)
        self.user_id = user_id
        await self.feedback_call(f"Парсер принял запрос, артикул {article}")

        page = await self._new_page()
        await page.goto(self.url, wait_until="load")
        await self.feedback_call("Загрузил страницу!")
        await asyncio.sleep(15)

        try:
            await self.feedback_call("Перезагружаем страницу, так надо...")
            await page.reload()

            await asyncio.sleep(1.5)

            await page.evaluate(self.scroll_down)
            await page.locator('div[style*="grid-template-columns: repeat(9, minmax(56px, 90px));"]').click(delay=1)

            counter = 0
            links_lenght = 0

            while True:
                links_lenght = len(self.links)
                await self._parse_html(page=page)
                print(f"EARN {len(self.links)} LINKS")
                await self.feedback_call(f"Собрано {len(self.links)} фотографии!")
                await page.keyboard.press("PageDown", delay=0.8)
                sleep = random.uniform(1.5, 3.5)
                await asyncio.sleep(sleep)
                if links_lenght == len(self.links):
                    counter +=1
                else:
                    counter = 0
                if counter > 3:
                    await self.feedback_call(f"Собраны все фотоозывы!")
                    break

            await page.close()

        except Exception:
            await self.feedback_call("Невозможно загрузить отзывы! Попробуйте позже!")
            await page.close()
            raise HTTPException(
                status_code=436,
                detail="Unavailable reviews"
            )



    async def return_links(self):
        for resolution in self.wc:
            for link in self.links:
                address = self.links[link]
                if resolution in address:
                    self.links[link] = address.replace(resolution, "/wc1200/")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{DETECTOR}:9090/model/detect",
                json={
                    "user_id": self.user_id,
                    "images": list(self.links.values())
                }
            ) as resp:
                if resp.status == 200:
                    return True


    async def __aenter__(self):
        """Async context manager.
        
        Example:
        >>> async with ParserService() as parser:
        >>>     await parser.parse(24896184303)
        """
        self.pl = await self.pl_ctx.start()
        return self

    async def __aexit__(self, *args):
        await self.pl.stop()