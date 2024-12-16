import datetime
import re
import copy

import dateutil
import dateutil.parser

from job_seeking_agent.crawler.markdown import MarkdownTableCrawler, MultiMarkdownTableCrawler

class SimplifyGitHubCrawler:
    def __init__(self, url: str, name_map: dict):
        self.url = url
        self.name_map = name_map

    def __iter__(self):
        markdown_crawler = MarkdownTableCrawler(self.url)
        last_row_data = None
        header = None

        for i, row in enumerate(markdown_crawler):
            row_data = [col.strip().lower() for col in row.split('|')]

            if i == 0:
                header = row_data
                print(header)
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

            html_link_res = re.search(r"href=\"(.+)\"", application_link)
            if html_link_res:
                application_link = html_link_res.group(1)
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


class SWECollegeJobCrawler:
    def __init__(self, url: str, name_map: dict):
        self.url = url
        self.name_map = name_map

    def __iter__(self):
        markdown_crawler = MultiMarkdownTableCrawler(self.url)

        for table in markdown_crawler:
            header = None
            for i, row in enumerate(table):
                row_data = [col.strip().lower() for col in row.split('|')]

                if i == 0:
                    header = row_data
                    print(header)
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
                html_link_res = re.search(r"\<a href=\"(.+)\"\>", application_link)
                if html_link_res:
                    application_link = html_link_res.group(1)
                row_data[link_index] = application_link

                # process date
                date_index = header.index(self.name_map["date"])
                days = row_data[date_index]
                match_res = re.match("(\d+)d", days)
                if match_res:
                    days = int(match_res.group(1))
                post_date = datetime.date.today() - datetime.timedelta(days=days)
                row_data[date_index] = post_date

                yield {k: row_data[header.index(v)] for k, v in self.name_map.items() if v in header}


if __name__ == "__main__":
    summer = SimplifyGitHubCrawler(
        url="https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README.md",
        name_map={
            "company": "company",
            "role": "role",
            "location": "location",
            "link": "application/link",
            "date": "date posted"
        }
    )

    off_season = SimplifyGitHubCrawler(
        url="https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README-Off-Season.md",
        name_map={
            "company": "company",
            "role": "role",
            "location": "location",
            "season": "terms",
            "link": "application/link",
            "date": "date posted"
        }
    )

    intl = SWECollegeJobCrawler(
        url="https://github.com/speedyapply/2025-SWE-College-Jobs/raw/refs/heads/main/INTERN_INTL.md",
        name_map={
            "company": "company",
            "role": "position",
            "location": "location",
            "link": "posting",
            "date": "age"
        }
    )

    rows = []

    for item in summer:
        if "canada" in item["location"]:
            rows.append(item)

    for item in off_season:
        if "canada" in item["location"]:
            rows.append(item)

    for item in intl:
        if "canada" in item["location"]:
            rows.append(item)

    import pandas as pd
    pd.DataFrame(rows).to_csv("intern.csv", index=False)
