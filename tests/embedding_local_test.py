import json
import numpy as np
from job_seeker.chunking.base import chunk_html
from job_seeker.embedding.sentence_transformer_embedding import (
    request_embedding,
    request_cross_embedding,
)


def bi_encoder_test():
    from job_seeker.scraper.microsoft import MicrosoftScraper

    pages = [
        "https://jobs.careers.microsoft.com/global/en/job/1695161/Research-Intern---AI-Infrastructure",
        "https://jobs.careers.microsoft.com/global/en/job/1775087/Research-Intern---Agent-Systems-for-AI-Infrastructure",
        "https://jobs.careers.microsoft.com/global/en/job/1755598/",
        "https://jobs.careers.microsoft.com/global/en/job/1796829/Finance-Manager",
    ]

    with open("resume.json") as f:
        resume = json.load(f)
    resume_embeddings = {
        key: [request_embedding(text) for text in texts]
        for key, texts in resume.items()
    }

    for page in pages:
        print(f"Scraping {page}")
        m = MicrosoftScraper(page)
        page_chunks = chunk_html(m())
        job_embeddings = [request_embedding(chunk.text) for chunk in page_chunks]

        for key, embedding_list in resume_embeddings.items():
            total_max_similarity = 0
            for i, resume_embedding in enumerate(embedding_list):
                max_similarity = 0
                max_index = 0
                for j, job_embedding in enumerate(job_embeddings):
                    cosine_similarity = np.dot(resume_embedding, job_embedding) / (
                        np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
                    )
                    if cosine_similarity > max_similarity:
                        max_similarity = cosine_similarity
                        max_index = j
                total_max_similarity = max(max_similarity, total_max_similarity)
                print(f"{key}{i}, max: {max_similarity}")


def cross_encoder_test():
    from job_seeker.scraper.microsoft import MicrosoftScraper

    pages = [
        "https://jobs.careers.microsoft.com/global/en/job/1695161/Research-Intern---AI-Infrastructure",
        "https://jobs.careers.microsoft.com/global/en/job/1775087/Research-Intern---Agent-Systems-for-AI-Infrastructure",
        "https://jobs.careers.microsoft.com/global/en/job/1755598/",
        "https://jobs.careers.microsoft.com/global/en/job/1796829/Finance-Manager",
    ]

    with open("resume.json") as f:
        resume = json.load(f)

    for page in pages:
        print(f"Scraping {page}")
        m = MicrosoftScraper(page)
        page_chunks = chunk_html(m())

        for key, text_list in resume.items():
            total_max_similarity = 0
            for i, query in enumerate(text_list):
                max_similarity = 0
                max_index = 0
                for j, context in enumerate(page_chunks):
                    cosine_similarity = request_cross_embedding(query, context.text)
                    if cosine_similarity > max_similarity:
                        max_similarity = cosine_similarity
                        max_index = j
                total_max_similarity = max(max_similarity, total_max_similarity)
                print(f"{key}{i}, max: {max_similarity}")


bi_encoder_test()
cross_encoder_test()
