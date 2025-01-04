import asyncio
import time
import os

from dotenv import load_dotenv
from loguru import logger
import aio_pika

from job_seeker.crawler.base import CrawlerRegistry
from job_seeker.core.db.rabbitmq import publish

load_dotenv()


class LocalCrawlingDispatcher:
    def __init__(self, crawler_configs):
        self.crawler_configs = crawler_configs

    async def start_workers(self):
        futures = []
        for name in CrawlerRegistry.list():
            crawler = CrawlerRegistry.get(name)()
            futures.append(asyncio.create_task(crawler.serve()))

        await asyncio.gather(*futures)

    async def dispatch(self):
        worker_task = asyncio.create_task(self.start_workers())
        # TODO: if there is new crawler, cancel the worker_task and restart it
        logger.info("Start dispatching")
        while True:
            for config in self.crawler_configs:
                await publish(config["name"], config["link"])
            await asyncio.sleep(10)
        worker_task.cancel()


if __name__ == "__main__":
    crawler_configs = [
        {
            "name": "SimplifyGitHubCrawler",
            "link": "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README.md",
        },
        {
            "name": "SimplifyGitHubCrawler",
            "link": "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README-Off-Season.md",
        },
        {
            "name": "SWECollegeJobCrawler",
            "link": "https://github.com/speedyapply/2025-SWE-College-Jobs/raw/refs/heads/main/INTERN_INTL.md",
        },
        {
            "name": "CanadianTechCrawler",
            "link": "https://github.com/Dannny-Babs/Canadian-Tech-Internships-2025/raw/refs/heads/main/README.md",
        },
    ]

    dispatcher = LocalCrawlingDispatcher(crawler_configs)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dispatcher.dispatch())
    loop.close()
