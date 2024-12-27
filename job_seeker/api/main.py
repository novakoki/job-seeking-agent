import asyncio
import os

import pika
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()


async def crawling_timer():
    while True:
        connection = pika.BlockingConnection(pika.URLParameters(os.environ.get("RABBITMQ_URL")))
        channel = connection.channel()
        channel.queue_declare(queue='crawling')
        channel.basic_publish(exchange='', routing_key='crawling', body='start')
        connection.close()
        await asyncio.sleep(10)


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(crawling_timer())
