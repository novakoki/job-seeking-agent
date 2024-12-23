import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from job_seeker.utils.singleton import SingletonMeta

class RequestsScraper:
    def __call__(self, url, attrs):
        with requests.get(url) as response:
            soup = BeautifulSoup(response.text)
            job_detail = soup.find(attrs=attrs)

            return str(job_detail)

class PlaywrightScraper(metaclass=SingletonMeta):
    def __init__(self):
        self.playwright = None
        self.browser = None

    def __call__(self, url, selector):
        if self.browser is None:
            self.playwright = sync_playwright().start()
            chromium = self.playwright.chromium
            self.browser = chromium.launch(headless=True)
        page = self.browser.new_page()
        page.goto(url)
        page.wait_for_load_state()
        page.wait_for_selector(selector)
        details = page.locator(selector).inner_html()
        page.close()
        return details

    def __del__(self):
        if self.browser is not None:
            self.browser.close()
            self.playwright.stop()

play_wright_scraper = PlaywrightScraper()
