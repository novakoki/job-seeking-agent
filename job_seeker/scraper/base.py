from abc import ABC, abstractmethod
import time
import json

import requests
import aiohttp
from playwright.async_api import async_playwright
from loguru import logger

from job_seeker.chunking.clean_html import clean_html
from job_seeker.db.dao import JobDAO
from job_seeker.db.rabbitmq import consume, publish


class BaseScraper(ABC):
    @abstractmethod
    async def extract(self, link: str) -> str:
        ...

    async def serve(self):
        queue_name = self.__class__.__name__
        await consume(queue_name, self.execute)

    async def execute(self, msg: str):
        msg = json.loads(msg)
        link = msg["link"]
        job_id = msg["job_id"]
        logger.info(f"Consume link: {link}")
        job = await JobDAO.find_one(job_id)
        if job is None:
            logger.error(f"job_id does not exist: {job_id}")
            return
        start = time.time()
        try:
            desc = await self.extract(link)
            logger.info(
                f"Scrape {link} with page length {len(desc)} in {time.time() - start:.2f} seconds"
            )
            await publish("chunking", json.dumps({"job_id": job_id, "desc": desc}))
        except Exception as e:
            logger.error(f"Error scraping {link}: {e}")


class RequestsScraper(BaseScraper):
    def extract(self, url) -> str:
        with requests.get(url) as response:
            return response.text


class AiohttpScraper(BaseScraper):
    async def extract(self, url) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                job_detail = await response.text()

                return job_detail


class PlaywrightScraper(BaseScraper):
    def __init__(self, page):
        self.page = page

    async def extract(self, url) -> str:
        page = self.page
        await page.goto(url)
        await page.wait_for_load_state()
        await page.wait_for_timeout(5000)
        details = await page.locator("body").inner_html()
        return details


class ScraperRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, scraper: type[BaseScraper]):
        if name in cls._registry:
            raise ValueError(f"{name} already exists in the registry")
        cls._registry[name] = scraper

    @classmethod
    def get(cls, name: str) -> type[BaseScraper]:
        if name not in cls._registry:
            raise ValueError(f"{name} not found in the registry")
        return cls._registry.get(name)

    @classmethod
    def list(cls):
        return cls._registry.keys()


ScraperRegistry.register("RequestsScraper", RequestsScraper)
ScraperRegistry.register("AiohttpScraper", AiohttpScraper)
ScraperRegistry.register("PlaywrightScraper", PlaywrightScraper)
