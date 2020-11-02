from riotwatcher import ApiError
import discord
import api_static_data
import post_embeds
import get_summoner
import asyncio
import api_request as api
import traceback
import datetime


lol_watcher = api_static_data.lol_watcher

api_key = api_static_data.riot_api_key


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        channel = client.get_channel(api_static_data.log_channel_id)
        await channel.send("Bot online")

    async def on_message(self, message):
        if message.content.startswith("!game"):
            username = message.content[6:]
            playerList = await post_embeds.SetTeams(username)
            if(playerList.response == api.ResType.SUCCESS):
                await message.channel.send("Match found, processing")
                await post_embeds.makeEmbeds(message, playerList.data)
            elif(playerList.response == api.ResType.NODATA):
                await message.channel.send("Match not found")

        elif message.content.startswith("!player"):
            username = message.content[8:]
            player = await post_embeds.GetSummoner(username)
            if(player.response == api.ResType.SUCCESS):
                await message.channel.send("player found")
            elif(player.response == api.ResType.NODATA):
                await message.channel.send("player not found")

        elif message.content.startswith("!rank"):
            checkRankName = message.content[6:]
            summoner = api.GetSummonerWithId(checkRankName)
            if(summoner.response == api.ResType.SUCCESS):
                rank = api.GetRankWithId(summoner.data['id'])
                if(rank.response == api.ResType.SUCCESS):
                    await message.channel.send(rank.data)

        elif message.content.startswith("!champ"):
            championName = message.content[7:]
            await message.channel.send(get_summoner.GetChampion(championName))

    async def on_error(event, *args, **kwargs):
        embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c)
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        channel = client.get_channel(api_static_data.log_channel_id)
        await channel.send(embed=embed)


client = MyClient()
loop = asyncio.get_event_loop()
loop.run_until_complete(client.start(
    api_static_data.discord_bot_token))
