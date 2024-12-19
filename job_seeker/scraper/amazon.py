import requests
from bs4 import BeautifulSoup

class AmazonScraper:
    def __init__(self, url):
        self.url = url

    def __call__(self):
        with requests.get(self.url) as response:
            soup = BeautifulSoup(response.text)
            job_detail = soup.find(attrs={"id": "job-detail-body"})
            return job_detail.get_text("\n")
        

if __name__ == "__main__":
    a = AmazonScraper("https://amazon.jobs/en/jobs/2850218/system-development-engineer-internship-2025-can?utm_source=simplify&ref=simplify")
    print(a())