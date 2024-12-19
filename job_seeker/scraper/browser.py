from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from job_seeker.utils.singleton import SingletonMeta

class PlaywrightScraper(metaclass=SingletonMeta):
    def __init__(self):
        self.browser = None

    async def __call__(self, url, selector):
        async with async_playwright() as playwright:
            if self.browser is None:
                chromium = playwright.chromium
                self.browser = await chromium.launch(headless=True)
            page = await self.browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state()
            await page.wait_for_selector(selector)
            details = await page.locator(selector).inner_html()
            soup = BeautifulSoup(details)
            await page.close()
            return soup.get_text("\n")
