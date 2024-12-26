import time

from loguru import logger
from pydantic import ValidationError

from job_seeker.crawler.base import CrawlerRegistry
from job_seeker.db.connection import job_collection
from job_seeker.db.model import Job

class CrawlingDispatcher:
    def __init__(self, crawler_configs):
        self.crawler_configs = crawler_configs

    async def run(self):
        start = time.time()
        futures = []
        for crawler_config in self.crawler_configs:
            crawler_class = CrawlerRegistry.get(crawler_config["name"])
            crawler = crawler_class()
            async for job in crawler.extract_jobs(crawler_config["link"]):
                try:
                    Job.model_validate(job)
                except ValidationError as e:
                    logger.error(f"Error validating job: {job}, {e}")
                    continue
                # workaround for the lack of transaction support in MongoDB
                future = job_collection.update_one(
                    filter={"link": job["link"]},
                    update={"$set": job},
                    upsert=True
                )
                futures.append(future)
        cnt = 0
        for future in futures:
            result = await future
            if not result.matched_count:
                cnt += 1
        logger.info(f"crawled {cnt} new jobs, time cost: {time.time() - start}")


if __name__ == "__main__":
    async def main():
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
        await dispatcher.run()
        

    import asyncio
    asyncio.run(main())
        # import pandas as pd
        # pd.DataFrame(rows).sort_values(["location", "company"]).to_csv("intern.csv", index=False)
