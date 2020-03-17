import os
import uuid
import asyncio
from azure.servicebus.aio import QueueClient, Message

namespace = os.environ['SERVICE_BUS_HOSTNAME']
sender_constr = os.environ['SENDER_CONNECTION_STR']


async def main(count: int):
    queue_client: QueueClient = QueueClient.from_connection_string(
        sender_constr, 'simplequeue')
    msg = Message(body='This is the message content')

    for index in range(count):
        msg = Message(f'New Message {index}')
        msg.properties.content_type = 'text/plain'
        msg.properties.message_id = uuid.uuid4().hex
        await queue_client.send(msg)

if __name__ == "__main__":
    asyncio.run(main(count=10))
