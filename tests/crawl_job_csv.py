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

from job_seeker.crawler.base import CrawlerRegistry
import pandas as pd

async def main():
    results = []
    for crawler_config in crawler_configs:
        crawler_class = CrawlerRegistry.get(crawler_config["name"])
        crawler = crawler_class()

        async for job in crawler.extract_jobs(crawler_config["link"]):
            if "canada" in job.location.lower():
                job.source = crawler.__class__.__name__
                results.append(job.model_dump(exclude={"id"}))
    
    pd.DataFrame(results).to_csv("canada_jobs.csv", index=False)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
