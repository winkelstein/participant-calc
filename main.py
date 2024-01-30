import asyncio
import os
import csv

from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)


# Setting configuration values
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Create the client and connect
client = TelegramClient('session', api_id=API_ID, api_hash=API_HASH)


async def main():
    await client.start()
    print("Client Created")

    user_input_channel = input("enter entity(telegram URL or entity id):")

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset = 0
    limit = 100
    all_participants = []

    print('Fetching all the users...')

    while True:
        participants = await client(GetParticipantsRequest(
            my_channel, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    print('Writing to user_data.csv...')

    with open('user_data.csv', 'w', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=[
                                'id', 'first_name', 'last_name', 'username'])

        writer.writeheader()
        for participant in all_participants:
            writer.writerow({"id": participant.id, "first_name": participant.first_name, "last_name": participant.last_name,
                             "username": participant.username})

with client:
    client.loop.run_until_complete(main())
