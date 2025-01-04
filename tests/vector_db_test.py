import json

from job_seeker.embedding.sentence_transformer_embedding import request_embedding
from job_seeker.core.db.dao import ChunkEmbeddingDAO, JobDAO


async def test_request_embedding():
    with open("resume.json", "r") as f:
        data = json.load(f)

    results = dict()

    for key, value in data.items():
        if key != "experience":
            continue
        for text in value if isinstance(value, list) else [value]:
            embedding = request_embedding(text)

            print(text, len(embedding))

            response = await ChunkEmbeddingDAO.search(embedding, top_k=200)

            for point in response.points:
                job = await JobDAO.find_one(point.payload["job_id"])
                # if job is not None and "canada" in job.location.lower():
                if (job.role, job.company, job.location, job.date, job.link) not in results:
                    results[(job.role, job.company, job.location, job.date, job.link)] = [(key, point.score)]
                else:
                    results[(job.role, job.company, job.location, job.date, job.link)].append((key, point.score))

    import pandas as pd
    df = pd.DataFrame(
        (key[0], key[1], key[2], key[3], key[4], sorted(value, key=lambda x:x[1], reverse=True), sum([x[1] for x in value]))
         for key, value in results.items()
    ).sort_values(by=[6, 2], ascending=False)
    df.to_csv("results.csv", index=False)



if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_request_embedding())
    loop.close()
