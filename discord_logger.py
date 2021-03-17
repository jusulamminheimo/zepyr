from enum import IntEnum
import datetime
import discord
import zepyr_config as asd

client: discord.Client


async def log(message: str):
    global client
    dt = datetime.datetime.utcnow()
    timeStamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    msg_with_timestamp = message+" ["+timeStamp+"]"
    print(msg_with_timestamp)
    channel = client.get_channel(asd.log_channel_id)
    await channel.send(f"```{msg_with_timestamp}```")


async def log_multi(message: str):
    """ends with ```"""
    global client
    dt = datetime.datetime.utcnow()
    timeStamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    msg_with_timestamp = message+"["+timeStamp+"]```"
    print(msg_with_timestamp)
    channel = client.get_channel(asd.log_channel_id)
    await channel.send(f"{msg_with_timestamp}")
