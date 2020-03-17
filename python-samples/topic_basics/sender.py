import asyncio
import os
import uuid
import random
from azure.servicebus.aio import TopicClient, Message

sender_constr = os.environ['SENDER_CONNECTION_STR']


async def main(count: int):
    topic_client: TopicClient = TopicClient.from_connection_string(
        sender_constr, name="simpletopic", debug=False)

    for index in range(count):
        msg = Message(f"New topic message {index}")
        msg.properties.message_id = uuid.uuid4().hex
        msg.properties.content_type = random.choice(
            ['application/json', 'text/plain'])
        msg.properties.subject = 'content'

        await topic_client.send(msg)


if __name__ == "__main__":
    asyncio.run(main(10))
