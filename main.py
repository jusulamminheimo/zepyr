from riotwatcher import ApiError
import discord
import config_file
import post_embeds
import get_summoner
import asyncio
import api_request as api
import traceback
import datetime
import discord_logger as dlogger
import sys

lol_watcher = config_file.lol_watcher

api_key = config_file.riot_api_key


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        channel = client.get_channel(config_file.log_channel_id)
        await channel.send("Bot online")

    async def on_message(self, message):
        if message.content.startswith("!game"):
            username = message.content[6:]
            player_list = await post_embeds.set_teams(username)
            if(player_list.response == api.ResType.SUCCESS):
                await message.channel.send("Match found, processing")
                await post_embeds.make_embeds(message, player_list.data)
            elif(player_list.response == api.ResType.NODATA):
                await message.channel.send("Match not found")
            elif(player_list.response == api.ResType.DENIED):
                await message.channel.send("API KEY EXPIRED")

        elif message.content.startswith("!rank"):
            checkRankName = message.content[6:]
            summoner = await api.get_summoner_by_summonername(checkRankName)
            if(summoner.response == api.ResType.SUCCESS):
                rank = await api.get_rank_with_summonerid(summoner.data['id'])
                if(rank.response == api.ResType.SUCCESS):
                    await message.channel.send(rank.data)

    async def on_error(event, *args, **kwargs):
        embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c)
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        channel = client.get_channel(config_file.log_channel_id)
        await channel.send(embed=embed)
        sys.stdout.flush()


client = MyClient()
dlogger.client = client
loop = asyncio.get_event_loop()
loop.run_until_complete(client.start(
    config_file.discord_bot_token))
