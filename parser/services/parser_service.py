import asyncio
import re
import random
from playwright.async_api import async_playwright
from fastapi.exceptions import HTTPException


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


    def __init__(self) -> None:
        self.links = dict()


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


    async def parse(self, article: int):
        self.url = "https://www.ozon.ru/product/" + str(article)

        page = await self._new_page()
        await page.goto(self.url, wait_until="load")
        await asyncio.sleep(5)

        try:
            await page.evaluate(self.scroll_down)
            await page.locator('div[style*="grid-template-columns: repeat(9, minmax(56px, 90px));"]').click(delay=1)

            await asyncio.sleep(1.7)
        except TimeoutError:
            print("RELOAD PAGE")
            await page.reload()

            await page.evaluate(self.scroll_down)
            await page.locator('div[style*="grid-template-columns: repeat(9, minmax(56px, 90px));"]').click(delay=1)

            await asyncio.sleep(1.7)
        finally:
            counter = 0
            links_lenght = 0

            while True:
                links_lenght = len(self.links)
                await self._parse_html(page=page)
                print(f"EARN {len(self.links)} LINKS")
                await page.keyboard.press("PageDown", delay=0.8)
                sleep = random.uniform(1.5, 3.5)
                await asyncio.sleep(sleep)
                if links_lenght == len(self.links):
                    counter +=1
                else:
                    counter = 0
                if counter > 3:
                    break

            await page.close()


    def return_links(self):
        for resolution in self.wc:
            for link in self.links:
                address = self.links[link]
                if resolution in address:
                    self.links[link] = address.replace(resolution, "/wc1200/")

        return self.links


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