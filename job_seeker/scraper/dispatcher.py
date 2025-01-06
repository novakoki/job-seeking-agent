import asyncio
import json

from loguru import logger

from job_seeker.core.db.dao import JobDAO
from job_seeker.core.db.rabbitmq import publish, get_queue_size


class LocalPlaywrightScraperDispatcher:
    async def dispatch(self):
        logger.info("Start dispatching")
        while True:
            while True:
                scrape_size = await get_queue_size("PlaywrightScraper")
                if scrape_size == 0:
                    chunking_size = await get_queue_size("chunking")
                    if chunking_size == 0:
                        break
                await asyncio.sleep(60)

            async for job in JobDAO.watch_job_without_desc():
                job_id = job.id
                link = job.link
                await publish(
                    "PlaywrightScraper", json.dumps({"job_id": job_id, "link": link})
                )


if __name__ == "__main__":

    async def main():
        from job_seeker.scraper.worker import LocalPlaywrightScraperWorker

        worker = LocalPlaywrightScraperWorker()
        worker_task = asyncio.create_task(worker.serve())
        dispatcher = LocalPlaywrightScraperDispatcher()
        await dispatcher.dispatch()
        worker_task.cancel()

    asyncio.run(main())
