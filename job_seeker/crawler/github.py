import datetime
import re

from loguru import logger
import dateutil
import dateutil.parser

from job_seeker.crawler.base import BaseCrawler, CrawlerRegistry
from job_seeker.crawler.markdown import extract_markdown_table, extract_markdown_multi_table
from job_seeker.db.model import Job
from job_seeker.utils.async_utils import async_enumerate

class SimplifyGitHubCrawler(BaseCrawler):
    def __init__(self):
        self.name_map = {
           "company": "Company",
            "role": "Role",
            "location": "Location",
            "season": "Terms",
            "link": "Application/Link",
            "date": "Date Posted"
        }

    async def extract_jobs(self, link):
        logger.info(f"Extracting jobs from {link}")
        last_row_data = None
        header = None

        async for i, row in async_enumerate(extract_markdown_table(link)):
            row_data = [col.strip() for col in row.split('|')]

            if i == 0:
                header = row_data
                logger.info(f"Table header: {header}")
                continue

            if i == 1:
                continue
            
            # process company name
            company_index = header.index(self.name_map["company"])
            company_name = row_data[company_index]
            if company_name == "↳":
                company_name = last_row_data[company_index]
            md_link_res = re.search(r'\[(.+)\]', company_name)
            if md_link_res:
                company_name = md_link_res.group(1)
            row_data[company_index] = company_name

            # process application link
            link_index = header.index(self.name_map["link"])
            application_link = row_data[link_index]
            if application_link == "🔒":
                application_link = ""
            html_link_res = re.search(r'\<a href=\"(.+?)\"\>', application_link)
            if html_link_res:
                application_link = html_link_res.group(1)
            if not application_link:
                continue
            application_link = application_link.replace("utm_source=Simplify&ref=Simplify", "")
            if application_link.endswith("&") or application_link.endswith("?"):
                application_link = application_link[:-1]
            row_data[link_index] = application_link

            # process date
            date_index = header.index(self.name_map["date"])
            post_date = row_data[date_index]
            post_date = dateutil.parser.parse(post_date)
            if (last_row_data is not None
                and application_link == last_row_data[link_index]
                and post_date > last_row_data[date_index]
            ):
                post_date = post_date.replace(year=post_date.year-1)
            row_data[date_index] = post_date

            last_row_data = row_data

            yield {k: row_data[header.index(v)] for k, v in self.name_map.items() if v in header}


class SWECollegeJobCrawler(BaseCrawler):
    def __init__(self):
        self.name_map = {
            "company": "Company",
            "role": "Position",
            "location": "Location",
            "link": "Posting",
            "date": "Age"
        }

    async def extract_jobs(self, link):
        logger.info(f"Extracting jobs from {link}")
        async for table in extract_markdown_multi_table(link):
            header = None
            for i, row in enumerate(table):
                row_data = [col.strip() for col in row.split('|')]

                if i == 0:
                    header = row_data
                    logger.info(f"Table header: {header}")
                    continue

                if i == 1:
                    continue

                 # process company name
                company_index = header.index(self.name_map["company"])
                company_name = row_data[company_index]
                html_link_res = re.search(r"\<strong\>(.+)\<\/strong\>", company_name)
                if html_link_res:
                    company_name = html_link_res.group(1)
                row_data[company_index] = company_name

                # process application link
                link_index = header.index(self.name_map["link"])
                application_link = row_data[link_index]
                html_link_res = re.search(r"\<a href=\"(.+?)\"\>", application_link)
                if html_link_res:
                    application_link = html_link_res.group(1)
                if not application_link:
                    continue
                row_data[link_index] = application_link

                # process date
                date_index = header.index(self.name_map["date"])
                days = row_data[date_index]
                match_res = re.match("(\d+)d", days)
                if match_res:
                    days = int(match_res.group(1))
                post_date = datetime.datetime.today() - datetime.timedelta(days=days)
                row_data[date_index] = post_date

                yield {k: row_data[header.index(v)] for k, v in self.name_map.items() if v in header}


class CanadianTechCrawler(BaseCrawler):
    def __init__(self):
        self.name_map = {
            "company": "Name",
            "role": "Notes",
            "location": "Location",
            "link": "Name",
            "date": "Date Posted"
        }

    async def extract_jobs(self, link):
        logger.info(f"Extracting jobs from {link}")
        last_row_data_dict = None
        header = None

        async for i, row in async_enumerate(extract_markdown_table(link)):
            row_data = [col.strip() for col in row.split('|')]

            if i == 0:
                header = row_data
                logger.info(f"Table header: {header}")
                continue

            if i == 1:
                continue

            row_data_dict = {k: row_data[header.index(v)] for k, v in self.name_map.items() if v in header}
            
            # process company name
            company_index = header.index(self.name_map["company"])
            company_name = row_data[company_index]
            md_link_res = re.search(r'\[(.+)\]', company_name)
            if md_link_res:
                company_name = md_link_res.group(1)
            row_data_dict["company"] = company_name

            # process application link
            link_index = header.index(self.name_map["link"])
            application_link = row_data[link_index]
            md_link_res = re.search(r'\((.+)\)', application_link)
            if md_link_res:
                application_link = md_link_res.group(1)
            if not application_link:
                continue
            row_data_dict["link"] = application_link

            # process date
            date_index = header.index(self.name_map["date"])
            post_date = row_data[date_index]
            try:
                post_date = dateutil.parser.parse(post_date)
            except:
                if last_row_data_dict:
                    post_date = last_row_data_dict["date"]
                else:
                    post_date = None
            row_data_dict["date"] = post_date

            last_row_data_dict = row_data_dict

            yield row_data_dict

CrawlerRegistry.register("SimplifyGitHubCrawler", SimplifyGitHubCrawler)
CrawlerRegistry.register("SWECollegeJobCrawler", SWECollegeJobCrawler)
CrawlerRegistry.register("CanadianTechCrawler", CanadianTechCrawler)

