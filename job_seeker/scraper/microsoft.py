from job_seeker.scraper.browser import PlaywrightScraper

class MicrosoftScraper:
    def __init__(self, url):
        self.url = url
        self.selector = ".SearchJobDetailsCard"

    async def __call__(self):
        scraper = PlaywrightScraper()
        content = await scraper(self.url, self.selector)
        # print(content)
        return content


if __name__ == "__main__":
    import asyncio
    url = "https://jobs.careers.microsoft.com/global/en/job/1755598/"
    a = MicrosoftScraper(url, ".SearchJobDetailsCard")
    asyncio.run(a())
