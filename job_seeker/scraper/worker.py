import asyncio
import json
from typing import List

from loguru import logger
from playwright.async_api import async_playwright

from job_seeker.scraper.base import PlaywrightScraper
from job_seeker.db.rabbitmq import publish


class LocalPlaywrightScraperWorker:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page_index = 0
        self.page_num = 2
        self.scrapers: List[PlaywrightScraper] = []

    async def serve(self):
        logger.info("Start serving")
        self.playwright = await async_playwright().start()
        chromium = self.playwright.chromium
        self.browser = await chromium.launch(headless=True)
        for _ in range(self.page_num):
            page_instance = await self.browser.new_page()
            self.scrapers.append(PlaywrightScraper(page_instance))
        futures = []
        for scraper in self.scrapers:
            futures.append(asyncio.create_task(scraper.serve()))
        for future in futures:
            await future


if __name__ == "__main__":
    worker = LocalPlaywrightScraperWorker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.serve())
    loop.close()
