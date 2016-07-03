import discord
import aiohttp
from discord.ext import commands


class Overwatch:
    """Overwatch statistics."""

    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://owapi.net/api/v2/u/"

    @commands.command(name="ow", aliases=["overwatch"])
    async def ow(self, battletag):
        """Gets overwatch quick play statistics. Usage: `[p]ow battletag#1234`"""

        if "-" in battletag:
            await self.bot.say("Please specify `battletag#1234`")
            return
        battletag = battletag.replace("#", "-")
        user_api = self.api_url + battletag.capitalize() + "/stats/general"

        try:
            with aiohttp.ClientSession() as session:
                async with session.get(user_api) as api:
                    ow = await api.json()
        except:
            await self.bot.say("Unable to connect to Overwatch API.")
            return

        if ow == 500:
            await self.bot.say("Unable to retrieve data from Overwatch API, error 500 (Internal Server Error).")
            return

        error = ow.get("error", "")
        msg = ow.get("msg", "")
        p_battletag = battletag.capitalize().replace("-", "#")

        if error:
            await self.bot.say("Overwatch API returned: {} {}".format(error, msg))
            return

        owos = ow.get("overall_stats", None)
        owgs = ow.get("game_stats", None)

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

    @commands.command(name="owc", aliases=["owcomp"])
    async def owc(self, battletag):
        """Gets overwatch competitive statistics. Usage: `[p]owc battletag#1234`"""

        if "-" in battletag:
            await self.bot.say("Please specify `battletag#1234`")
            return
        battletag = battletag.replace("#", "-")
        user_api = self.api_url + battletag.capitalize() + "/stats/competitive"

        try:
            with aiohttp.ClientSession() as session:
                async with session.get(user_api) as api:
                    ow = await api.json()
        except:
            await self.bot.say("Unable to connect to Overwatch API.")
            return

        if ow == 500:
            await self.bot.say("Unable to retrieve data from Overwatch API, error 500 (Internal Server Error).")
            return

        error = ow.get("error", "")
        msg = ow.get("msg", "")
        p_battletag = battletag.capitalize().replace("-", "#")

        if error:
            if msg == "competitive stats not found":
                await self.bot.say("Player {} has no stats on competitive, not enough games played.".format(p_battletag))
                return
            await self.bot.say("Overwatch API returned: {} {}".format(error, msg))
            return

        owos = ow.get("overall_stats", None)
        owgs = ow.get("game_stats", None)

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
