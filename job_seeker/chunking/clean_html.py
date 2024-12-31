from bs4 import BeautifulSoup, Comment


def clean_html(html):
    soup = BeautifulSoup(html)
    unused_tags = ["script", "style", "svg", "image", "iframe", "code", "noscript"]
    for tag_name in unused_tags:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    for tag in soup.find_all(True):
        tag.attrs.clear()

    cleaned_html = "".join(line.strip() for line in soup.prettify().splitlines() if line.strip())
    cleaned_text = "\n".join(line.strip() for line in soup.get_text().splitlines() if line.strip())
    
    return cleaned_html, cleaned_text

if __name__ == "__main__":
    async def main():
        from job_seeker.scraper.base import PlaywrightScraper
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            scraper = PlaywrightScraper(page)
            html = await scraper.extract("https://aexp.eightfold.ai/careers/job/24674562")
            a, b = clean_html(html)
            print(a)
            print(b)

    import asyncio
    asyncio.run(main())
