from logging import error
from discord import player
from riotwatcher import LolWatcher, ApiError
import discord
import get_win_ratio
import api_static_data
import time
import get_summoner
import api_request as api


baseUrl = "https://static.wikia.nocookie.net/leagueoflegends/images/"
rankIconIron = baseUrl + "0/03/Season_2019_-_Iron_1.png"
rankIconBronze = baseUrl + "f/f4/Season_2019_-_Bronze_1.png"
rankIconSilver = baseUrl + "7/70/Season_2019_-_Silver_1.png"
rankIconGold = baseUrl + "9/96/Season_2019_-_Gold_1.png"
rankIconPlatinum = baseUrl + "7/74/Season_2019_-_Platinum_1.png"
rankIconDiamond = baseUrl + "9/91/Season_2019_-_Diamond_1.png"
rankIconMaster = baseUrl + "1/11/Season_2019_-_Master_1.png"
rankIconGrandmaster = baseUrl + "7/76/Season_2019_-_Grandmaster_1.png"
rankIconChallenger = baseUrl + "5/5f/Season_2019_-_Challenger_1.png"


def get_rank_icon(rank_str):
    if rank_str:
        lowerCaseRank = rank_str.lower()
        if "iron" in lowerCaseRank:
            return rankIconIron
        elif "bronze" in lowerCaseRank:
            return rankIconBronze
        elif "silver" in lowerCaseRank:
            return rankIconSilver
        elif "gold" in lowerCaseRank:
            return rankIconGold
        elif "platinum" in lowerCaseRank:
            return rankIconPlatinum
        elif "diamond" in lowerCaseRank:
            return rankIconDiamond
        elif "grand" in lowerCaseRank:
            return rankIconGrandmaster
        elif "master" in lowerCaseRank:
            return rankIconMaster
        elif "challenger" in lowerCaseRank:
            return rankIconChallenger
    else:
        return ""


async def update_embeds(posted_embeds, embed_list, player_list):
    for x in range(10):  # update embeds
        newEmbed = discord.Embed()
        name = player_list[x]._username
        fixedName = name.replace(' ', '+')
        linkToOpGG = "https://euw.op.gg/summoner/userName="+fixedName.lower()

        nameWithChamp = player_list[x]._champion+" - "+name

        if x < 5:
            newEmbed.color = 0xff0033
        else:
            newEmbed.color = 0x085eff

        if 'None' in player_list[x]._rank:
            rank = "UNRANKED"
        else:
            rank = player_list[x]._rank

        winRatioString = "WR "+str(get_win_ratio.get_win_ratio(
            player_list[x]._username, player_list[x]._championId, api_static_data.lol_watcher))
        if 'None' in winRatioString:
            wrString = 'No games'
        else:
            wrString = winRatioString
        newEmbed.set_author(name=nameWithChamp, url=linkToOpGG,  icon_url=str(
            "http://ddragon.leagueoflegends.com/cdn/" + api_static_data.latest + "/img/champion/" + player_list[x]._champion + ".png"))
        newEmbed.set_footer(text=rank+" ("+str(wrString)+")", icon_url=str(
            get_rank_icon(player_list[x]._rank)))
        embed_list.append(newEmbed)
        await posted_embeds[x].edit(embed=newEmbed)


async def post_embeds(ctx, embed_list):
    postedEmbeds = []
    for x in range(10):  # post embeds without winratios
        ebd = await ctx.channel.send(embed=embed_list[x])
        postedEmbeds.append(ebd)
        if(x == 4):
            await ctx.channel.send("- VS -")
    return postedEmbeds


async def make_embeds(message, player_list):
    embed_list = []

    for x in range(10):
        newEmbed = discord.Embed()

        if x < 5:
            newEmbed.color = 0xff0033
        else:
            newEmbed.color = 0x085eff

        name = player_list[x]._username
        fixedName = name.replace(' ', '+')
        linkToOpGG = "https://euw.op.gg/summoner/userName="+fixedName.lower()

        nameWithChamp = player_list[x]._champion+" - "+name

        if 'None' in player_list[x]._rank:
            rank = "UNRANKED"
        else:
            rank = player_list[x]._rank

        newEmbed.set_author(name=nameWithChamp, url=linkToOpGG,  icon_url=str(
            "http://ddragon.leagueoflegends.com/cdn/" + api_static_data.latest + "/img/champion/" + player_list[x]._champion + ".png"))
        newEmbed.set_footer(text=rank, icon_url=str(
            get_rank_icon(player_list[x]._rank)))
        embed_list.append(newEmbed)

    print("embeds created")

    posted_embeds = await post_embeds(message, embed_list)

    print("embeds posted")

    await update_embeds(posted_embeds, embed_list, player_list)


# global readable match data
match_global = api.ApiResponse(None, 0, api.ResType.NULL)


async def get_summoner(summoner_name):
    summoner = api.get_player_by_summonername(summoner_name)

    if summoner.response == api.ResType.WAIT:
        time.sleep(summoner.waitTime+1)
        summoner = api.get_player_by_summonername(summoner_name)

    if(summoner.response == api.ResType.NODATA):
        return summoner

    elif(summoner.response == api.ResType.SUCCESS):
        return summoner


async def set_teams(summoner_name):
    summoner = api.get_player_by_summonername(summoner_name)
    if summoner.response == api.ResType.WAIT:
        time.sleep(summoner.wait_time)
        summoner = api.get_player_by_summonername(summoner_name)

    if(summoner.response == api.ResType.SUCCESS):
        match = api.get_match_by_summonerid(summoner.data['id'])
        if match.response == api.ResType.WAIT:
            time.sleep(match.waitTime)
            match = api.get_match(summoner.data['id'])

        elif(match.response == api.ResType.SUCCESS):
            participant_list = match.data['participants']
            player_list = []
            for players in participant_list:
                playerTemp = {'summonerName': players['summonerName'],
                              'summonerId': players['summonerId'], 'championId': players['championId']}
                player = api.get_player_by_summonername(playerTemp)
                player_list.append(player)

            match.data = player_list
            return match

        elif(match.response == api.ResType.NODATA):
            return match

    elif(summoner.response == api.ResType.NODATA):
        return summoner
