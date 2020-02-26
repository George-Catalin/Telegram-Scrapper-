from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import csv
import random
import time
import numpy as np

input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

mode = int(input("Enter 1 to send by user ID or 2 to send by username: "))

messages = ["Hello {}, How are you?", "Hi {}, What's up?", "Hey {}, do you want to gotrained?"]

for user in users:
    if mode == 2:
        if user['username'] == "":
            continue
        receiver = client.get_input_entity(user['username'])
    elif mode == 1:
        receiver = InputPeerUser(user['id'], user['access_hash'])
    else:
        print("Invalid Mode. Exiting.")
        client.disconnect()
        sys.exit()
    message = random.choice(messages)
    try:
        print("Sending Message to:", user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue
client.disconnect()
print("Done. Message sent to all users.")