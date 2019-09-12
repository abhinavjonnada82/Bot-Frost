import requests
from discord.ext import commands
import discord
import json
import datetime
import pytz
import math

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
husker_schedule = []
huskerbot_footer="Generated by HuskerBot"


class StatBot(commands.Cog, name="CFB Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def seasonstats(self, ctx, year=2019):
        """ Returns current season stats """

        msg = await ctx.send("Loading...")

        url = "https://api.collegefootballdata.com/stats/season?year={}&team=nebraska".format(year)

        try:
            r = requests.get(url)
            seasonstats_json = r.json()
        except:
            await ctx.send("An error occurred retrieving poll data.")
            return

        dump = True
        if dump:
            with open("seasonstats_json.json", "w") as fp:
                json.dump(seasonstats_json, fp, sort_keys=True, indent=4)
            fp.close()

        message_string = "```\n{} Season Stats for Nebraska\n".format(year)
        for stat in seasonstats_json:
            if stat["statName"] == "possessionTime":
                message_string += "{:<22} : {}\n".format(stat["statName"], datetime.timedelta(seconds=math.floor(stat["statValue"] / 60)))
            else:
                message_string += "{:<22} : {}\n".format(stat["statName"], stat["statValue"])

        message_string += "\n```"

        await msg.edit(content=message_string)

    @commands.command(aliases=["mu",])
    async def matchup(self, ctx, *, team):
        """ Shows matchup history between Nebraska and another team. """
        url = "https://api.collegefootballdata.com/teams/matchup?team1=nebraska&team2={}".format(team)

        try:
            r = requests.get(url)
            matchup_json = r.json()
        except:
            await ctx.send("An error occurred retrieving poll data.")
            return

        dump = True
        if dump:
            with open("matchup_json.json", "w") as fp:
                json.dump(matchup_json, fp, sort_keys=True, indent=4)
            fp.close()

        msg = await ctx.send("Loading...")

        embed = discord.Embed(title="Match up history between Nebraska and {}".format(team.capitalize()), color=0xFF0000)
        embed.set_thumbnail(url="https://i.imgur.com/aaqkw35.png")

        embed.add_field(name="{} Wins".format(matchup_json["team1"]), value=matchup_json["team1Wins"], inline=False)
        embed.add_field(name="{} Wins".format(matchup_json["team2"]), value=matchup_json["team2Wins"], inline=False)
        if matchup_json["ties"]:
            embed.add_field(name="Ties", value=matchup_json["ties"], inline=False)

        gameHistLen = len(matchup_json["games"])
        gameHistLen -= 1

        game_datetime_raw = datetime.datetime.strptime(matchup_json["games"][gameHistLen]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        game_datetime_utc = pytz.utc.localize(game_datetime_raw)
        game_datetime_cst = game_datetime_utc.astimezone(pytz.timezone("America/Chicago"))

        embed.add_field(name="Most Recent Match Up", value="Date: {}\nLocation: {}\n{} : {} - {} : {}\n".format(
            str(game_datetime_cst)[:-15],
            matchup_json["games"][gameHistLen]["venue"],
            matchup_json["games"][gameHistLen]["homeTeam"],
            matchup_json["games"][gameHistLen]["homeScore"],
            matchup_json["games"][gameHistLen]["awayScore"],
            matchup_json["games"][gameHistLen]["awayTeam"]))
        await msg.edit(content="", embed=embed)


    # TODO Maybe have option to pick from various polls. Use reactions?
    @commands.command(aliases=["polls",])
    async def poll(self, ctx, year=2019, week=None, seasonType=None):
        """ Returns current Top 25 ranking from the Coach's Poll, AP Poll, and College Football Playoff ranking.
        Usage is: `$poll <year> <week>"""

        url = "https://api.collegefootballdata.com/rankings?year={}".format(year)

        if not seasonType:
            url = url + "&seasonType=regular"
        else:
            url = url + "&seasonType=postseason"

        if week:
            url = url + "&week={}".format(week)

        try:
            r = requests.get(url)
            poll_json = r.json()
        except:
            await ctx.send("An error occurred retrieving poll data.")
            return

        dump = True
        if dump:
            with open("cfb_polls.json", "w") as fp:
                json.dump(poll_json, fp, sort_keys=True, indent=4)
            fp.close()

        embed = discord.Embed(title="{} {} Season Week {} Poll".format(poll_json[0]['season'], str(poll_json[0]['seasonType']).capitalize(), poll_json[0]['week']), color=0xFF0000)

        ap_poll_raw = poll_json[0]['polls'][0]['ranks']
        last_rank = 1

        x = 0
        y = 0
        while x < len(ap_poll_raw):
            while y < len(ap_poll_raw):
                print("Raw Rank: {}, Last Rank: {}".format(ap_poll_raw[y]['rank'], last_rank))
                if ap_poll_raw[y]['rank'] == last_rank:
                    if ap_poll_raw[y]['firstPlaceVotes']:
                        embed.add_field(name="#{} {}".format(ap_poll_raw[y]['rank'], ap_poll_raw[y]['school']), value="{}\nPoints: {}\nFirst Place Votes: {}".format(ap_poll_raw[y]['conference'], ap_poll_raw[y]['points'], ap_poll_raw[y]['firstPlaceVotes']))
                    else:
                        embed.add_field(name="#{} {}".format(ap_poll_raw[y]['rank'], ap_poll_raw[y]['school']), value="{}\nPoints: {}".format(ap_poll_raw[y]['conference'], ap_poll_raw[y]['points']))
                    last_rank += 1
                    y = 0
                    break
                y += 1
            x += 1

        await ctx.send(embed=embed)

    # TODO Discord 2,000 char limit per message really limits this command. Need to make output more readable. Possibly add ability to filter by offense, defense, special teams, etc.
    @commands.command()
    async def roster(self, ctx, team="NEBRASKA", year=2019):
        """ Returns the current roster """
        await ctx.send("This command is under construction.")
        return

    # TODO This need to be reworked. Home and away teams don't have the same length of stats.
    @commands.command(aliases=["bs",])
    async def boxscore(self, ctx, year: int, week: int):
        """ Returns the box score of the searched for game. """

        if not type(year) is int:
            await ctx.send("You must enter a numerical year.")
            return
        elif year < 2004:
            await ctx.send("Data is not available prior to 2004.")
            return

        if not type(week) is int:
            await ctx.send("You must enter a numerical week.")
            return

        edit_msg = await ctx.send("Loading...")

        url = "https://api.collegefootballdata.com/games/teams?year={}&week={}&seasonType=regular&team=nebraska".format(year, week)

        try:
            r = requests.get(url)
            boxscore_json = r.json() # Actually imports a list
        except:
            await ctx.send("An error occurred retrieving boxscore data.")
            return

        if not boxscore_json:
            await ctx.send("This was a bye week. Try again.")
            return

        dump = False
        if dump:
            with open("boxscore_json.json", "w") as fp:
                json.dump(boxscore_json, fp, sort_keys=True, indent=4)
            fp.close()

        statFullName = {"rushingTDs": "Rushing TDs", "puntReturnYards": "Punt Return Yards", "puntReturnTDs": "Punt Return TDs", "puntReturns": "Punt Returns", "passingTDs": "Passing TDs",
                         "interceptionYards": "Interception Yards", "interceptionTDs": "Interception TDs", "passesIntercepted": "Passes Intercepted", "fumblesRecovered": "Fumbles Recovered",
                         "totalFumbles": "Total Fumbles", "tacklesForLoss": "Tackles For Loss", "defensiveTDs": "Defensive TDs", "tackles": "Tackles", "sacks": "Sacks", "qbHurries": "QB Hurries",
                         "passesDeflected": "Passes Deflected", "possessionTime": "Possesion Time", "interceptions": "Interceptions", "fumblesLost": "Fumbles Lost", "turnovers": "Turnovers",
                         "totalPenaltiesYards": "Total Penalties Yards", "yardsPerRushAttempt": "Yards Per Rush Attempt", "rushingAttempts": "Rushing Attempts", "rushingYards": "Rushing Yards",
                         "yardsPerPass": "Yards Per Pass", "kickReturnYards": "Kick Return Yards", "kickReturnTDs": "Kick Return TDs", "kickReturns": "Kick Returns", "completionAttempts": "Completion Attempts",
                         "netPassingYards": "Net Passing Yards", "totalYards": "Total Yards", "fourthDownEff": "Fourth Down Eff", "thirdDownEff": "Third Down Eff", "firstDowns": "First Downs"}

        home_stats = boxscore_json[0]["teams"][0]
        home_message = "{} ({})\n{}\n".format(home_stats["school"], home_stats["points"],"-" * 30)

        for stat in home_stats["stats"]:
            home_message += "{}\: {}\n".format(statFullName[stat["category"]], stat["stat"])

        await edit_msg.edit(content=home_message)

        away_stats = boxscore_json[0]["teams"][1]
        away_message = "{} ({})\n{}\n".format(away_stats["school"], away_stats["points"],"-" * 30)

        for stat in away_stats["stats"]:
            away_message += "{}\: {}\n".format(statFullName[stat["category"]], stat["stat"])

        await ctx.send(away_message)
        return


def setup(bot):
    bot.add_cog(StatBot(bot))