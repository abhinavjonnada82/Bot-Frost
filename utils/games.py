import datetime
import os

import requests
from bitlyshortener import Shortener
from bs4 import BeautifulSoup

from utils.consts import HEADERS
from utils.consts import TZ


class GameBets:
    game_number = None
    over_under = None
    spread = None
    win = None

    def __init__(self, game_number, over_under, spread, win):
        self.game_number = game_number
        self.over_under = over_under
        self.spread = spread
        self.win = win


class GameBetLine:
    provider = None
    spread = None
    formatted_spread = None
    over_under = None

    def __init__(self, provider=None, spread=None, formatted_spread=None, over_under=None):
        self.provider = provider
        self.spread = spread
        self.formatted_spread = formatted_spread
        self.over_under = over_under


class GameBetInfo:
    home_team = None
    home_score = None
    away_team = None
    away_score = None
    userbets = []
    lines = []

    def __init__(self, year, week, team, season="regular"):  # , home_team=None, home_score=None, away_team=None, away_score=None, lines=None):
        self.home_team = None
        self.home_score = None
        self.away_team = None
        self.away_score = None
        self.userbets = []
        self.lines = []

        self.establish(year, week, team, season)

    def establish(self, year, week, team, season="regular"):
        url = f"https://api.collegefootballdata.com/lines?year={year}&week={week}&seasonType={season}&team={team}"
        re = requests.get(url=url, headers=HEADERS)
        data = re.json()

        try:
            self.home_team = data[0]['homeTeam']
            self.home_score = data[0]['homeScore']
            self.away_team = data[0]['awayTeam']
            self.away_score = data[0]['awayScore']
            linedata = data[0]["lines"]

            for line in linedata:
                self.lines.append(
                    GameBetLine(
                        provider=line['provider'],
                        spread=line['spread'],
                        formatted_spread=line['formattedSpread'],
                        over_under=line['overUnder']
                    )
                )
        except:
            pass


class SeasonStats:
    wins = None
    losses = None

    def __init__(self, wins=0, losses=0):
        self.wins = wins
        self.losses = losses


class HuskerDotComSchedule:
    opponent = None
    game_date_time = None
    tv_station = None
    radio_station = None
    conference_game = False
    ranking = None
    outcome = None
    boxscore_url = None
    recap_url = None
    notes_url = None
    quotes_url = None
    history_url = None
    gallery_url = None
    location = None
    bets = GameBetInfo
    week = None
    opponent_url = None

    def __init__(self, opponent, game_date_time, tv_station, radio_station, conference_game, ranking, outcome, boxscore_url, recap_url, notes_url, quotes_url, history_url, gallery_url, location,
                 bets, week, opponent_url):
        self.opponent = opponent
        self.game_date_time = game_date_time
        self.tv_station = tv_station
        self.radio_station = radio_station
        self.conference_game = conference_game
        self.ranking = ranking
        self.outcome = outcome
        self.boxscore_url = boxscore_url
        self.recap_url = recap_url
        self.notes_url = notes_url
        self.quotes_url = quotes_url
        self.history_url = history_url
        self.gallery_url = gallery_url
        self.location = location
        self.bets = bets
        self.week = week
        self.opponent_url = opponent_url


def ScheduleBackup(year=datetime.datetime.now().year, shorten=False):
    r = requests.get(url=f"https://huskers.com/sports/football/schedule/{year}", headers=HEADERS)

    if not r.status_code == 200:
        return

    def shorten_url(url):
        bitly_oauth_token = [os.getenv("bitly_oauth")]
        shortener = Shortener(tokens=bitly_oauth_token, max_cache_size=128)
        return shortener.shorten_urls(long_urls=[url])[0]

    soup = BeautifulSoup(r.content, "html.parser")

    games_raw = soup.find_all("div", class_="sidearm-schedule-game-row flex flex-wrap flex-align-center row")
    games = []

    game_datetime_raw = ""
    game_week_raw = 0

    season_stats = SeasonStats()

    def opponent_url():
        all_games = soup.find_all(attrs={"class": "sidearm-schedule-game-opponent-name"})
        logos_raw = soup.find_all(attrs={"class": "sidearm-schedule-game-opponent-logo noprint"})
        logos = []

        if len(all_games) > len(logos_raw):
            logos.append("https://ucomm.unl.edu/images/brand-book/Our-marks/nebraska-n.jpg")

        for logo in logos_raw:
            logos.append("https://huskers.com/" + logo.contents[1].attrs["data-src"])

        del all_games
        del logos_raw

        return logos

    logos = opponent_url()

    for index, game in enumerate(games_raw):
        opponent = ""
        ranking = ""

        if index > 0:  # Games after the first week of the season
            game_datetime_raw = game.contents[1].contents[3].contents[1].text  # Current season? 2019?

            if game_datetime_raw == "":  # Seasons prior or after?
                game_datetime_raw = game.contents[1].contents[3].contents[3].contents[3].conents[1].text

            opponent = game.contents[1].contents[3].contents[3].contents[3].contents[0]

            if opponent == "\n":  # After the first week?
                opponent = game.contents[1].contents[3].contents[3].contents[3].contents[1].contents[0]

            if "#" in opponent:  # Ranked opponents?
                ranking = opponent
                opponent = game.contents[1].contents[3].contents[3].contents[3].contents[3].contents[0]

        elif index == 0:  # First game of the season. Usually the Spring game
            game_datetime_raw = game.contents[1].contents[1].contents[1].text  # Current season? 2019?

            if game_datetime_raw == "":  # Seasons prior or after
                game_datetime_raw = game.contents[1].contents[3].contents[1].contents[1].text

            try:  # Current season? 2019?
                opponent = game.contents[1].contents[1].contents[3].contents[3].contents[0]
            except IndexError:  # Seasons prior or after
                opponent = game.contents[1].contents[3].contents[3].contents[3].contents[1].contents[0]

        outcome = str(game.contents[5].contents[1].text).replace("\n", "").replace(",", ", ")
        outcome_found = ("L," in outcome) or ("W," in outcome)
        if not outcome_found:
            outcome = None

        opponent = str(opponent).replace("\r", "").replace("\n", "").lstrip().rstrip()
        game_datetime_raw = game_datetime_raw.split("\n")

        tv_stations = ["ESPN", "FOX", "FS1", "ABC", "BTN"]
        months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        big_ten_members = ["Indiana", "Maryland", "Michigan", "Michigan State", "Ohio State", "Peen State", "Rutgers", "Illinois", "Iowa", "Minnesota", "Nebraska", "Northwestern", "Purdue",
                           "Wisconsin"]
        raw_date = raw_time = _tv_station = _radio_station = _conference_game = ""

        for team in big_ten_members:
            if team == opponent:
                _conference_game = True

        for ele in game_datetime_raw:
            if ele[0:3].upper() in months:
                raw_date = ele.split(" (")[0] + ' ' + str(year)

            if ("PM" in ele) or ("AM" in ele) or ("A.M." in ele.upper()) or ("P.M." in ele.upper()):
                raw_time = ele.rstrip()

            # Fixing dirty data
            if "::" in raw_time:
                raw_time = raw_time.replace("::", ":")
            if " :" in raw_time:
                raw_time = raw_time.replace(" :", ":")
            if "." in raw_time:
                raw_time = raw_time.replace(".", "").upper()
                raw_time = raw_time[0:2] + ":00 " + raw_time[-2:]
            if ele == "TBA ":
                raw_time = "11:00 PM"

            if not raw_time:
                raw_time = "11:00 PM"

            if ele in tv_stations:
                _tv_station = ele.rstrip()

            if ele == "Husker Sports Network":
                _radio_station = "Huskers Sports Network"

        _game_date_time = datetime.datetime.strptime(f"{raw_date} {raw_time}", "%b %d %Y %I:%M %p").astimezone(tz=TZ)

        _game_links_raw = game.contents[5].contents[3].contents[1].contents

        _game_boxscore_url = _game_recap_url = _game_notes_url = _game_quotes_url = _game_gallery_url = _game_history_url = ""

        husker_url = "https://huskers.com"

        for ele in _game_links_raw:
            if not ele == '\n':
                if ele.text == 'History':
                    _game_history_url = shorten_url(husker_url + ele.contents[0].attrs['href']) if shorten else husker_url + ele.contents[0].attrs['href']
                elif ele.text == 'Box Score':
                    _game_boxscore_url = shorten_url(husker_url + ele.contents[0].attrs['href']) if shorten else husker_url + ele.contents[0].attrs['href']
                elif ele.text == 'Recap':
                    _game_recap_url = shorten_url(husker_url + ele.contents[0].attrs['href']) if shorten else husker_url + ele.contents[0].attrs['href']
                elif ele.text == 'Notes':
                    _game_notes_url = shorten_url(husker_url + ele.contents[0].attrs['href']) if shorten else husker_url + ele.contents[0].attrs['href']
                elif ele.text == 'Quotes':
                    _game_quotes_url = shorten_url(husker_url + ele.contents[0].attrs['href']) if shorten else husker_url + ele.contents[0].attrs['href']
                elif ele.text == 'Gallery':
                    _game_gallery_url = shorten_url(husker_url + ele.contents[0].attrs['href']) if shorten else husker_url + ele.contents[0].attrs['href']

        # Credit to: https://stackoverflow.com/questions/22726860/beautifulsoup-webscraping-find-all-finding-exact-match
        loc = soup.find_all(lambda tag: tag.name == "div" and tag.get("class") == ["sidearm-schedule-game-location"])
        states_old = {"Ala.": "AL", "Alaska": "AK", "Ariz.": "AZ", "Ark.": "AR", "Calif.": "CA", "Colo.": "CO", "Conn.": "CT", "Del.": "DE", "D.C.": "DC", "Fla.": "FL", "Ga.": "GA", "Hawaii": "HI",
                      "Idaho": "ID", "Ill.": "IL", "Ind.": "IN", "Iowa": "IA", "Kan.": "KS", "Ky.": "KY", "La.": "LA", "Maine": "ME", "Md.": "MD", "Mass.": "MA", "Mich.": "MI", "Minn.": "MN",
                      "Miss.": "MS", "Mo.": "MO", "Mont.": "MT", "Neb.": "NE", "Nev.": "NV", "N.H.": "NH", "N.J.": "NJ", "N.M.": "NM", "N.Y.": "NY", "N.C.": "NC", "N.D.": "ND", "Ohio": "OH",
                      "Okla.": "OK", "Ore.": "OR", "Pa.": "PA", "R.I.": "RI", "S.C.": "SC", "S.D.": "SD", "Tenn.": "TN", "Texas": "TX", "Utah": "UT", "Vt.": "VT", "Va.": "VA", "Wash.": "WA",
                      "W.Va.": "WV", "Wis.": "WI", "Wyo.": "WY"}

        def game_location(index):
            if loc[index].text.strip() == "Memorial Stadium":
                return ["Lincoln", "NE"]
            else:
                city_state = loc[index].text.strip().split(", ")

                city = city_state[0]
                state = ""

                if len(city_state) == 2:
                    try:
                        state = states_old[city_state[1]]
                    except KeyError:
                        state = "N/A"
                    except:
                        state = "N/A"
                elif len(city_state) == 1:
                    state = "NE"
                return [city, state]

        if "spring" not in opponent.lower():
            game_week_raw += 1

        try:
            games.append(
                HuskerDotComSchedule(
                    opponent=opponent,
                    game_date_time=_game_date_time,
                    tv_station=_tv_station,
                    radio_station=_radio_station,
                    conference_game=_conference_game,
                    ranking=ranking,
                    outcome=outcome,
                    boxscore_url=_game_boxscore_url,
                    recap_url=_game_recap_url,
                    notes_url=_game_notes_url,
                    quotes_url=_game_quotes_url,
                    history_url=_game_history_url,
                    gallery_url=_game_gallery_url,
                    location=game_location(index),
                    bets=GameBetInfo(year=_game_date_time.year, team="Nebraska", week=index + 1, season="regular"),
                    week=game_week_raw,
                    opponent_url=logos[game_week_raw]
                )
            )
        except IndexError:
            print("Hmmmm")

        if outcome is not None:
            if "W" in outcome:
                season_stats.wins += 1
            elif "L" in outcome:
                season_stats.losses += 1

    # Clean up variables
    del opponent
    del _game_date_time
    del _tv_station
    del _radio_station
    del _conference_game
    del ranking
    del outcome
    del _game_boxscore_url
    del _game_recap_url
    del _game_notes_url
    del _game_quotes_url
    del _game_history_url
    del _game_gallery_url
    del _game_links_raw
    del big_ten_members
    del ele
    del game_datetime_raw
    del game
    del games_raw
    del husker_url
    del index
    del loc
    del months
    del outcome_found
    del r
    del raw_date
    del raw_time
    del shorten
    del soup
    del states_old
    del team
    del tv_stations
    del year

    return games, season_stats


def Venue():
    r = requests.get("https://api.collegefootballdata.com/venues")
    return r.json()
