from job_seeker.scraper.base import RequestsScraper


class AmazonScraper:
    def __init__(self, url):
        self.url = url

    def __call__(self):
        scraper = RequestsScraper()
        return scraper(self.url, {"id": "job-detail-body"})


if __name__ == "__main__":
    a = AmazonScraper(
        "https://amazon.jobs/en/jobs/2850218/system-development-engineer-internship-2025-can?utm_source=simplify&ref=simplify"
    )
    print(a())
