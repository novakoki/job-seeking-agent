import asyncio
import json

from job_seeker.db.dao import JobDAO
from job_seeker.db.rabbitmq import publish


class LocalPlaywrightScraperDispatcher:
    async def dispatch(self):
        async for change in JobDAO.watch():
            if change["operationType"] == "insert":
                job_id = str(change["fullDocument"]["_id"])
                url = change["fullDocument"]["link"]
                await publish(
                    "PlaywrightScraper", json.dumps({"job_id": job_id, "link": url})
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
