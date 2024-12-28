import requests
import aiohttp
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from job_seeker.utils.singleton import SingletonMeta

class RequestsScraper:
    def __call__(self, url, attrs):
        with requests.get(url) as response:
            soup = BeautifulSoup(response.text)
            job_detail = soup.find(attrs=attrs)

            return str(job_detail)
        
class AiohttpScraper:
    async def __call__(self, url, attrs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text())
                job_detail = soup.find(attrs=attrs)

                return str(job_detail)


class PlaywrightScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None

    async def init(self):
        self.playwright = await async_playwright().start()
        chromium = self.playwright.chromium
        self.browser = await chromium.launch(headless=True)

    async def extract_page(self, url, selector="body") -> str:
        page = await self.browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state()
        if selector == "body":
            await page.wait_for_timeout(5000)
        await page.wait_for_selector(selector)
        details = await page.locator(selector).inner_html()
        # TODO: clean html
        await page.close()
        return details

    async def close(self):
        if self.browser is not None:
            self.browser.close()
            self.playwright.stop()
