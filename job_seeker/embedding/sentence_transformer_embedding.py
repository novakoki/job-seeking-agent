import requests

def request_embedding(text: str):
    with requests.post("http://192.168.1.74:8000/embedding/", json={"query": text}) as response:
        body = response.json()
    return body["embedding"]

def request_cross_embedding(query: str, context: str):
    with requests.post("http://192.168.1.74:8000/cross_embedding/", json={"query": query, "context": context}) as response:
        body = response.json()
    return body["similarity"]
