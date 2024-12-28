import asyncio
import time
import os

from dotenv import load_dotenv
from loguru import logger

from job_seeker.db.dao import JobDAO
from job_seeker.scraper.base import PlaywrightScraper

load_dotenv()

class ScraperDispatcher:
    def __init__(self):
        self.scraper = PlaywrightScraper()

    async def listen(self):
        async for change in JobDAO.watch():
            if change["operationType"] == "insert":
                await self.execute(change["fullDocument"]["_id"], change["fullDocument"]["link"])
            # print(change)

    async def execute(self, job_id, url):
        content = await self.scraper.extract_page(url)

        await JobDAO.update_desc(job_id, content)


if __name__ == "__main__":
    dispatcher = ScraperDispatcher()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dispatcher.listen())
    loop.close()
