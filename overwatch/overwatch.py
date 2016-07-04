"""
Overwatch cog by Phantium
https://github.com/phantium/phantium-cogs
"""

import discord
import aiohttp
from datetime import datetime
from discord.ext import commands

cache = None

# Player data cache time
cache_time = 1800

class Overwatch:
    """Overwatch statistics."""

    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://owapi.net/api/v2/u/"

    async def caching(self, ctx, type, battletag):
        battletag = battletag.replace("#", "-")
        user_api = self.api_url + battletag + "/stats/" + type

        global cache
        global cache_time

        if not cache:
            cache = {}
        if not cache.get(type):
            cache[type] = {}

        if cache[type].get(battletag):

            # Cleanup old cache items when the command is called
            c_remove = {}
            for count, (types, players) in enumerate(cache.items()):
                for player, data in players.items():
                    currenttime = ctx.message.timestamp
                    elapsedtime = currenttime - datetime.strptime(data["updated"], '%Y-%m-%d %H:%M:%S.%f')
                    if elapsedtime.seconds >= cache_time:
                        c_remove[count] = {type: {"player": player}}

            for c_index, c_expired in c_remove.items():
                for c_type, c_battletag in c_expired.items():
                    del cache[c_type][c_battletag["player"]]

            if elapsedtime.seconds >= cache_time:
                try:
                    with aiohttp.ClientSession() as session:
                        async with session.get(user_api) as api:
                            ow = await api.json()

                    cache[type][battletag] = {}
                    cache[type][battletag]["updated"] = str(ctx.message.timestamp)
                    cache[type][battletag]["data"] = {}
                    cache[type][battletag]["data"] = ow
                except:
                    return {"error": 408, "msg": "Connection to Overwatch API timed out"}
        else:
            try:
                with aiohttp.ClientSession() as session:
                    async with session.get(user_api) as api:
                        ow = await api.json()
            except:
                return {"error": 408, "msg": "Connection to Overwatch API timed out"}

            if ow == 500:
                return {"error": 500, "msg": "Internal Server Error"}

            error = ow.get("error")
            msg = ow.get("msg")
            if error:
                return {"error": error, "msg": msg}

            cache[type][battletag] = {}
            cache[type][battletag]["updated"] = str(ctx.message.timestamp)
            cache[type][battletag]["data"] = {}
            cache[type][battletag]["data"] = ow

        return cache[type]


    @commands.command(pass_context=True, name="ow", aliases=["overwatch"])
    async def ow(self, ctx, battletag):
        """Gets overwatch quick play statistics."""

        if "-" in battletag:
            await self.bot.say("Please specify `battletag#1234`")
            return

        # Get quick play cache
        cache = await self.caching(ctx, "general", battletag)

        error = cache.get("error")
        msg = cache.get("msg")
        if error:
            await self.bot.say("Error {}: {}".format(error, msg.title()))
            return

        battletag = battletag.replace("#", "-")
        owos = cache[battletag]["data"]["overall_stats"]
        owgs = cache[battletag]["data"]["game_stats"]

        p_battletag = battletag.replace("-", "#")
        p_level = owos.get("level", 0)
        p_rank = str(owos.get("comprank", "0")).replace("None", "Unranked")
        p_kills = int(owgs.get("solo_kills", 0))
        p_eliminations = int(owgs.get("eliminations", 0))
        p_damage = int(owgs.get("damage_done", 0))
        p_healing = int(owgs.get("healing_done", 0))
        p_deaths = int(owgs.get("deaths", 0))
        p_kpd = owgs.get("kpd", 0)
        p_winrate = owos.get("win_rate", 0)
        p_games = owos.get("games", 0)
        p_medals = int(owgs.get("medals", 0))
        p_medals_gold = int(owgs.get("medals_gold", 0))
        p_medals_silver = int(owgs.get("medals_silver", 0))
        p_medals_bronze = int(owgs.get("medals_bronze", 0))

        message = "```Overwatch (Quick Play) stats for {}```\n```Level: {}\nSkill Rating: {}\nKills: {:,}\nEliminations: {:,}\n" \
                  "Deaths: {:,}\nK/D: {}\nDamage done: {:,}\nHealing done: {:,}\nWinrate: {}%\nGames played: {:,}\nMedals earned: {:,} (G: {:,} S: {:,} B: {:,})```".format(
            p_battletag, p_level, p_rank, p_kills, p_eliminations, p_deaths,
            p_kpd, p_damage, p_healing, p_winrate, p_games, p_medals,
            p_medals_gold, p_medals_silver, p_medals_bronze)

        await self.bot.say(message)

    @commands.command(pass_context=True, name="owc", aliases=["owcomp"])
    async def owc(self, ctx, battletag):
        """Gets overwatch competitive statistics."""

        if "-" in battletag:
            await self.bot.say("Please specify `battletag#1234`")
            return

        # Get competitive cache
        cache = await self.caching(ctx, "competitive", battletag)

        error = cache.get("error")
        msg = cache.get("msg")
        if error:
            await self.bot.say("Error {}: {}".format(error, msg.title()))
            return

        battletag = battletag.replace("#", "-")
        battletag = battletag[0].upper() + battletag[1:]
        owos = cache[battletag]["data"]["overall_stats"]
        owgs = cache[battletag]["data"]["game_stats"]

        p_battletag = battletag.replace("-", "#")
        p_level = owos.get("level", 0)
        p_rank = str(owos.get("comprank", "0")).replace("None", "Unranked")
        p_kills = int(owgs.get("solo_kills", 0))
        p_eliminations = int(owgs.get("eliminations", 0))
        p_damage = int(owgs.get("damage_done", 0))
        p_healing = int(owgs.get("healing_done", 0))
        p_deaths = int(owgs.get("deaths", 0))
        p_kpd = owgs.get("kpd", 0)
        p_winrate = owos.get("win_rate", 0)
        p_games = owos.get("games", 0)
        p_medals = int(owgs.get("medals", 0))
        p_medals_gold = int(owgs.get("medals_gold", 0))
        p_medals_silver = int(owgs.get("medals_silver", 0))
        p_medals_bronze = int(owgs.get("medals_bronze", 0))

        message = "```Overwatch (Competitive) stats for {}```\n```Level: {}\nSkill Rating: {}\nKills: {:,}\nEliminations: {:,}\n" \
                  "Deaths: {:,}\nK/D: {}\nDamage done: {:,}\nHealing done: {:,}\nWinrate: {}%\nGames played: {:,}\nMedals earned: {:,} (G: {:,} S: {:,} B: {:,})```".format(
            p_battletag, p_level, p_rank, p_kills, p_eliminations, p_deaths,
            p_kpd, p_damage, p_healing, p_winrate, p_games, p_medals,
            p_medals_gold, p_medals_silver, p_medals_bronze)

        await self.bot.say(message)


def setup(bot):
    bot.add_cog(Overwatch(bot))
