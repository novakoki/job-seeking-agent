import os

from openai import AzureOpenAI
from dotenv import load_dotenv
from time import time

load_dotenv()

class OpenAIEmbedding:
    def __init__(self):
        self.client = AzureOpenAI()

    def __call__(self, input, save_name=None):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=input,
            encoding_format="float"
        )

        if save_name is None:
            save_name = "embedding_{}.json".format(time())

        with open(save_name, "w") as f:
            f.write(response.to_json(indent=0))

        return response

