import os
import asyncio
import pprint
from azure.servicebus.aio import QueueClient, Message

namespace = os.environ['SERVICE_BUS_HOSTNAME']
receiver_constr = os.environ['RECEIVER_CONNECTION_STR']


async def process_message(message: Message):
    print(message)
    print(f'Message ID: {message.properties.message_id} \n'
          f'{message.properties.group_sequence} \n'
          f'{message.properties.creation_time} \n'
          f'Content Type: {message.properties.content_type} \n'
          )

    # message.Size,
    # await message.complete()


async def main():
    queue_client = QueueClient.from_connection_string(
        receiver_constr, 'simplequeue')

    async with queue_client.get_receiver(idle_timeout=2) as receiver:
        async for message in receiver:
            await process_message(message)

if __name__ == "__main__":
    asyncio.run(main())
