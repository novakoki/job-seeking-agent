import asyncio
import time
import os

from dotenv import load_dotenv
from loguru import logger
import aio_pika

from job_seeker.crawler.base import CrawlerRegistry
from job_seeker.db.dao import JobDAO

load_dotenv()

class CrawlingDispatcher:
    def __init__(self, crawler_configs):
        self.crawler_configs = crawler_configs

    async def listen(self, loop):
        connection = await aio_pika.connect_robust(
            os.environ.get("RABBITMQ_URL"), loop=loop
        )

        async with connection:
            queue_name = "crawling"

            # Creating channel
            channel: aio_pika.abc.AbstractChannel = await connection.channel()

            # Declaring queue
            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(queue_name)

            async with queue.iterator() as queue_iter:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        await self.execute()

                        if queue.name in message.body.decode():
                            break

    async def execute(self):
        start = time.time()
        futures = []
        for crawler_config in self.crawler_configs:
            crawler_class = CrawlerRegistry.get(crawler_config["name"])
            crawler = crawler_class()
            async for job in crawler.extract_jobs(crawler_config["link"]):
                futures.append(asyncio.create_task(JobDAO.add_one(job)))
        cnt = 0
        for future in futures:
            try:
                result = await future
                if result is not None:
                    cnt += 1
            except Exception as e:
                logger.error(f"Failed to add job: {e}")
        logger.info(f"crawled {cnt} new jobs, time cost: {time.time() - start}")


if __name__ == "__main__":
    crawler_configs = [
        {
            "name": "SimplifyGitHubCrawler",
            "link": "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README.md"
        },
        {
            "name": "SimplifyGitHubCrawler",
            "link": "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README-Off-Season.md"
        },
        {
            "name": "SWECollegeJobCrawler",
            "link": "https://github.com/speedyapply/2025-SWE-College-Jobs/raw/refs/heads/main/INTERN_INTL.md"
        },
        {
            "name": "CanadianTechCrawler",
            "link": "https://github.com/Dannny-Babs/Canadian-Tech-Internships-2025/raw/refs/heads/main/README.md"
        }
    ]

    dispatcher = CrawlingDispatcher(crawler_configs)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dispatcher.listen(loop))
    loop.close()
