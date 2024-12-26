import re
import aiohttp


async def extract_markdown_table(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for line in response.content:
                result = re.match(r"\|(.+)\|", line.decode())
                if result:
                    yield result.group(1)


async def extract_markdown_multi_table(url):
    data = []
    valid = False
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for line in response.content:
                result = re.match(r"\|(.+)\|", line.decode())
                if result:
                    valid = True
                    data.append(result.group(1))
                else:
                    if valid:
                        yield data
                        valid = False
                        data.clear()
