import asyncio
import time
import os

from dotenv import load_dotenv
from loguru import logger

from job_seeker.db.dao import JobDAO

load_dotenv()

class ScraperDispatcher:
    def __init__(self):
        pass

    async def listen(self):
        async for change in JobDAO.watch():
            print(change)

    async def execute(self):
        pass


if __name__ == "__main__":
    dispatcher = ScraperDispatcher()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dispatcher.listen())
    loop.close()
