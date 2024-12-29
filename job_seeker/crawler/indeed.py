from playwright.sync_api import sync_playwright

from job_seeker.chunking.base import chunk_html

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]
    page.goto(
        "https://ca.indeed.com/jobs?q=software+intern&l=Canada&sort=date&from=searchOnDesktopSerp&vjk=5c1bc6ccb5b29bab"
    )
    details = page.locator("#mosaic-jobResults").inner_html()

for chunk in chunk_html(details):
    print(chunk)
