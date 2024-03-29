from riotwatcher import ApiError
import discord
import zepyr_config
import post_embeds
import get_summoner
import asyncio
import api_request as api
import traceback
import datetime
import discord_logger as dlogger
import aliases


lol_watcher = zepyr_config.lol_watcher

api_key = zepyr_config.riot_api_key


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        channel = client.get_channel(zepyr_config.log_channel_id)
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
                if(rank is not None):
                    await message.channel.send(rank.data)
                else:
                    await message.channel.send("No rank")


    async def on_error(self, event, *args, **kwargs):
        embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c)
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        channel = client.get_channel(zepyr_config.log_channel_id)
        await channel.send(embed=embed)


client = MyClient()
dlogger.client = client
loop = asyncio.get_event_loop()
loop.run_until_complete(client.start(
    zepyr_config.discord_bot_token))
