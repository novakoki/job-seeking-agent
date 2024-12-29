from typing import List

from openai import AzureOpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()


class OpenAIEmbedding:
    def __init__(self):
        self.client = AzureOpenAI()

    def encode(self, query: str) -> List[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small", input=query, encoding_format="float"
        )

        return np.array(response.data[0].embedding)


class OpenAIBatchEmbedding:
    def __init__(self):
        self.client = AzureOpenAI()

    def encode(self, queries: List[str]):
        raise NotImplementedError
