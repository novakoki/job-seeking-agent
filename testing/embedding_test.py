import tiktoken

from job_seeker.embedding.openai_embedding import OpenAIEmbedding
from job_seeker.scraper.microsoft import MicrosoftScraper


async def main():
#     encoding = tiktoken.encoding_for_model("text-embedding-3-small")
#     embedding = OpenAIEmbedding()

    a = MicrosoftScraper("https://jobs.careers.microsoft.com/global/en/job/1695161/Research-Intern---AI-Infrastructure")
    b = MicrosoftScraper("https://jobs.careers.microsoft.com/global/en/job/1775087/Research-Intern---Agent-Systems-for-AI-Infrastructure")
    c = MicrosoftScraper("https://jobs.careers.microsoft.com/global/en/job/1755598/")

    content = await asyncio.gather(
        a(), b(), c()
    )

    for i, item in enumerate(content):
        with open("job_{}.txt".format(i), "w") as f:
            f.write(item)

import asyncio
asyncio.run(main())
