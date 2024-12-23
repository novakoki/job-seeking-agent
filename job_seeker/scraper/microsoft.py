from job_seeker.scraper.base import play_wright_scraper

class MicrosoftScraper:
    def __init__(self, url):
        self.url = url
        self.selector = ".SearchJobDetailsCard"

    def __call__(self):
        content = play_wright_scraper(self.url, self.selector)
        return content


if __name__ == "__main__":
    url = "https://jobs.careers.microsoft.com/global/en/job/1755598/"
    a = MicrosoftScraper(url)
    print(a())
