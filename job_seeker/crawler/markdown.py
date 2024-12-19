from typing import Iterable

import re

import requests


class MarkdownTableCrawler(Iterable):
    def __init__(self, url):
        self.url = url

    def __iter__(self):
        with requests.get(self.url, stream=True) as response:
            for line in response.iter_lines():
                result = re.match(r"\|(.+)\|", line.decode())
                if result:
                    yield result.group(1)


class MultiMarkdownTableCrawler(Iterable):
    def __init__(self, url):
        self.url = url

    def __iter__(self):
        data = []
        valid = False
        with requests.get(self.url, stream=True) as response:
            for line in response.iter_lines():
                result = re.match(r"\|(.+)\|", line.decode())
                if result:
                    valid = True
                    data.append(result.group(1))
                else:
                    if valid:
                        yield data
                        valid = False
                        data.clear()
