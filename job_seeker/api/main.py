import asyncio

from job_seeker.crawler.dispatcher import LocalCrawlingDispatcher
from job_seeker.scraper.dispatcher import LocalPlaywrightScraperDispatcher
from job_seeker.scraper.worker import LocalPlaywrightScraperWorker
from job_seeker.chunking.worker import MultiprocessingChunkingWorker

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

async def main():
    # Initialize workers
    scraper_dispatcher = LocalPlaywrightScraperDispatcher()
    scraper_worker = LocalPlaywrightScraperWorker()
    chunking_worker = MultiprocessingChunkingWorker()
    crawling_dispatcher = LocalCrawlingDispatcher(crawler_configs)

    # Start workers
    bg_tasks = []
    bg_tasks.append(asyncio.create_task(scraper_dispatcher.dispatch()))
    bg_tasks.append(asyncio.create_task(scraper_worker.serve()))
    bg_tasks.append(asyncio.create_task(chunking_worker.serve()))
    bg_tasks.append(asyncio.create_task(crawling_dispatcher.dispatch()))

    # Start the dispatcher
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())