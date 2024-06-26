import sys
import re
import json
import asyncio
import random
from playwright.async_api import async_playwright as pl


assert sys.argv[1], "there is no args"
article = int(sys.argv[1])


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

links = dict()


async def parse_html(page):
    """Find all links in raw HTML by regular expression (re)."""

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
        if links.get(hashed_pic):
            continue
        else:
            links[hashed_pic] = el
    
    for el in thumbnails:
        hashed_thumb = el[32:-22]
        if links.get(hashed_thumb):
            continue
        else:
            links[hashed_thumb] = el


async def main(article: int):
    pl_ctx = await pl().start()

    browser = await pl_ctx.firefox.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    url = "https://www.ozon.ru/product/" + str(article)

    print(f"Going to {article} article")
    await page.goto(url, wait_until="load")
    await asyncio.sleep(1.5)

    print("Load page and wait some time")
    
    await page.evaluate(scroll_down)
    await page.locator('div[style*="grid-template-columns: repeat(9, minmax(56px, 90px));"]').click(delay=1)

    print("Click on locator")
    
    await asyncio.sleep(1)

    for _ in range(20):
        await parse_html(page=page)
        await page.keyboard.press("PageDown", delay=0.8)
        print(f"Earn {len(links)+1} links")
        sleep = random.uniform(1.5, 3)
        await asyncio.sleep(sleep)

    await page.close()
    await pl_ctx.stop()
    
    print("Close browser")

    with open('result.json', 'w') as fp:
        json.dump(links, fp)


if __name__ == "__main__":
    asyncio.run(main=main(article=article))
