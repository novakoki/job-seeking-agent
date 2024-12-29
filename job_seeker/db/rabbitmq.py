import aio_pika
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()


async def consume(queue_name, on_message):
    async def message_callback(message):
        async with message.process():
            await on_message(message.body.decode())

    connection = await aio_pika.connect(os.environ.get("RABBITMQ_URL"))

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # Declaring queue
        queue = await channel.declare_queue(
            queue_name,
            durable=True,
        )

        # Start listening the queue with name 'task_queue'
        await queue.consume(message_callback)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


async def publish(queue_name, message):
    connection = await aio_pika.connect(os.environ.get("RABBITMQ_URL"))

    async with connection:
        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(
            queue_name,
            durable=True,
        )

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name,
        )