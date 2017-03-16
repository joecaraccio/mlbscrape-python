"""Note: this is a temporary file before we decide where these methods should be implemented.
 It was only used for fixing the previous implementation of the database."""

from sql.hitter_entry import HitterEntry
from sql.pregame_hitter import PregameHitterGameEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.pitcher_entry import PitcherEntry
from sql.mlb_database import MlbDatabase
from sql.game import GameEntry
from mine.beautiful_soup_helper import get_soup_from_url
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
import datetime
from sql.umpire import UmpireCareerEntry
from mine.baseball_reference import team_dict, get_team_info
from mine.rotowire import rotowire_team_dict
import re
from bs4 import Comment
from sql.team_park import ParkEntry
from sqlalchemy import or_, and_

base_url = "http://gd2.mlb.com/components/game/mlb/year_2017/month_"

database_session = MlbDatabase().open_session()


def get_game_day_urls(game_date):
    game_urls = list()
    day_url = base_url + '%02d' % game_date.month + "/" + "day_" + '%02d' % game_date.day
    soup = get_soup_from_url(day_url)
    game_links = soup.findAll("a")
    for game_link in game_links:
        game_string = str(game_link.text).strip()
        if game_string.startswith("gid"):
            game_string = day_url + "/" + game_string + "linescore.xml"
            game_urls.append(game_string)
            print game_string

    return game_urls


def get_umpire_data():
    url = "https://swishanalytics.com/mlb/mlb-umpire-factors"
    umpire_soup = get_soup_from_url(url)

    stat_table = umpire_soup.find("table", {"id": "ump-table"}).find("tbody")

    if stat_table is not None:
        ump_rows = stat_table.findAll("tr")
        for ump_row in ump_rows:
            ump_data = ump_row.findAll("td")
            ump_entry = database_session.query(UmpireCareerEntry).get(str(ump_data[0].text.strip()))
            if ump_entry is None:
                ump_entry = UmpireCareerEntry(str(ump_data[0].text.strip()))

            ump_entry.ks_pct = float(ump_data[3].text.strip().replace("%", "")) / 100
            ump_entry.walks_pct = float(ump_data[4].text.strip().replace("%", "")) / 100
            ump_entry.runs_per_game = float(ump_data[5].text.strip())
            ump_entry.batting_average = float(ump_data[6].text.strip())
            ump_entry.on_base_pct = float(ump_data[7].text.strip())
            ump_entry.slugging_pct = float(ump_data[8].text.strip())

            ump_entry.ks_boost = float(ump_data[9].text.strip().replace("x", ""))
            ump_entry.walks_boost = float(ump_data[10].text.strip().replace("x", ""))
            ump_entry.runs_boost = float(ump_data[11].text.strip().replace("x", ""))
            ump_entry.batting_average_boost = float(ump_data[12].text.strip().replace("x", ""))
            ump_entry.on_base_pct_boost = float(ump_data[13].text.strip().replace("x", ""))
            ump_entry.slugging_pct_boost = float(ump_data[14].text.strip().replace("x", ""))

            try:
                database_session.add(ump_entry)
                database_session.commit()
            except IntegrityError:
                database_session.rollback()


def get_game_data(current_date):
    for team_key in team_dict:
        game_entries = database_session.query(GameEntry).filter(GameEntry.game_date == str(current_date),
                                                                or_(GameEntry.home_team == rotowire_team_dict.inv[team_dict[team_key]],
                                                                    GameEntry.away_team == rotowire_team_dict.inv[team_dict[team_key]]))
        if game_entries.count() != 0:
            continue
        team_abbrev = team_key
        day_url = "http://www.baseball-reference.com/boxes/" + team_abbrev + "/" + team_abbrev + \
                  str(current_date.year) + ("%02d" % current_date.month) + ("%02d" % current_date.day) + "0.shtml"

        boxscore_soup = get_soup_from_url(day_url)
        if boxscore_soup is None:
            continue

        # Get the home and away teams
        scorebox_section = boxscore_soup.find("div", {"class": "scorebox"})
        if scorebox_section is None:
            continue
        team_sections = scorebox_section.findAll("div")
        team_name_section = team_sections[6]
        if team_name_section is not None:
            home_team = team_name_section.find("strong").text.strip()
        team_name_section = team_sections[0]
        if team_name_section is not None:
            away_team = team_name_section.find("strong").text.strip()

        # Get the time
        time_section = boxscore_soup.find("div", {"class": "scorebox_meta"})
        game_time = time_section.findAll("div")[1].text
        game_time_final = re.search("\s[0-9]+:[0-9]+\s", game_time).group(0)

        time_components = game_time_final.split(":")
        if time_components[0] > 12:
            new_hour = int(time_components[0]) + 12

        game_time_final = str(new_hour) + ":" + time_components[1]

        section_headings = boxscore_soup.findAll("div", {"class": "section_heading"})

        for section_heading in section_headings:
            heading_section = section_heading.find("h2")
            if heading_section is not None:
                heading_text = heading_section.text.strip()
                if heading_text == "Other Info":
                    comments = heading_section.parent.parent.findAll(text=lambda text: isinstance(text, Comment))
                    for comment in comments:
                        umpire_match = re.search("Umpires:</strong> HP -\s[a-zA-Z']+\s[a-zA-Z']+", comment)
                        if umpire_match is not None:
                            umpire_name = umpire_match.group(0).replace("Umpires:</strong> HP - ", "")
                            weather_match = re.search("Start Time Weather:</strong>\s[0-9]+&deg;\sF", comment)
                            if weather_match is not None:
                                temperature_text = weather_match.group(0).replace("Start Time Weather:</strong>", "").replace("&deg; F", "").strip()
                            wind_match = re.search("Wind\s[0-9]+.+,", comment)
                            if wind_match is not None:
                                wind_text = re.findall(r'\d+', wind_match.group(0))[0]
                                wind_mulitplier = 0
                                if re.search(r"\bin\b", wind_match.group(0)):
                                    wind_mulitplier = -1
                                elif re.search(r"\bout\b", wind_match.group(0)):
                                    wind_mulitplier = 1
                                wind_int = wind_mulitplier*int(wind_text)
                            print current_date, game_time_final.strip(), rotowire_team_dict.inv[home_team], umpire_name, temperature_text, wind_int
                            game_entry = database_session.query(GameEntry).get((str(current_date), game_time_final.strip(), rotowire_team_dict.inv[home_team]))
                            if game_entry is None:
                                game_entry = GameEntry(str(current_date), game_time_final.strip(), rotowire_team_dict.inv[home_team], rotowire_team_dict.inv[away_team])
                                game_entry.umpire = umpire_name
                                game_entry.temperature = float(temperature_text)
                                game_entry.wind_speed = wind_int
                                #try:
                                database_session.add(game_entry)
                                database_session.commit()
                                #except IntegrityError:
                                #    print "Cannot find %s" % umpire_name
                                #    database_session.rollback()
                            else:
                                game_entry.game_date = str(current_date)
                                game_entry.game_time = game_time_final.strip()
                                game_entry.umpire = umpire_name
                                game_entry.temperature = float(temperature_text)
                                game_entry.wind_speed = wind_int
                                database_session.commit()

# TODO: need to lookup the home team so we can isolate the entries
"""itr=1
pregame_hitter_entries = database_session.query(PostgameHitterGameEntry).filter()
itr = pregame_hitter_entries.count()
for pregame_hitter_entry in pregame_hitter_entries:
    #pregame_hitter_entries = database_session.query(PostgamePitcherGameEntry).filter(PostgamePitcherGameEntry.game_date == game_entry.game_date,
    ###                                                                                   PostgamePitcherGameEntry.home_team == game_entry.home_team)
    print itr
    itr -= 1
    print pregame_hitter_entry.rotowire_id
    game_entry_query = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == pregame_hitter_entry.game_date,
                                                                             PregameHitterGameEntry.rotowire_id == pregame_hitter_entry.rotowire_id)
    if game_entry_query.count() > 0:
        pregame_hitter_entry.game_date = game_entry_query[0].game_date
        pregame_hitter_entry.game_time = game_entry_query[0].game_time
        pregame_hitter_entry.home_team = game_entry_query[0].home_team
        pregame_hitter_entry.is_home_team = game_entry_query[0].is_home_team
    else:
        continue
database_session.commit()
"""


for team_key in rotowire_team_dict:
    team_abbrev = team_key
    team_info = get_team_info(rotowire_team_dict[team_key], 2016)
    if team_info is not None:
        park_entry = ParkEntry(team_key, 2016)
        park_entry.park_hitter_score = team_info[0]
        park_entry.park_pitcher_score = team_info[1]
        try:
            database_session.add(park_entry)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()

"""
start_date = date(day=2, month=4, year=2016)
end_date = date(day=1, month=11, year=2016)
current_date = start_date
while current_date <= end_date:
    get_game_data(current_date)
    current_date += timedelta(days=1)
    game_urls = get_game_day_urls(current_date)
    for game_url in game_urls:
        game_soup = get_soup_from_url(game_url)
        game_time = datetime.datetime.strptime(game_soup.find("game").get("away_time") + " " + \
                                               game_soup.find("game").get("home_ampm"), '%I:%M %p').time()
        game_time = game_time.strftime('%H:%M')
        away_team_abbr = game_soup.find("game").get("away_name_abbrev")
        home_team_abbr = game_soup.find("game").get("home_name_abbrev")
        game_entry = GameEntry(str(current_date), game_time, home_team_abbr, away_team_abbr)
        try:
            database_session.add(game_entry)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            print home_team_abbr, away_team_abbr, game_time, str(current_date)
    current_date += timedelta(days=1)
    """

"""
database_session = MlbDatabase().open_session()

postgame_hitter_entries = database_session.query(PostgameHitterGameEntry)
for hitter in postgame_hitter_entries:
    game_entry = database_session.query(GameEntry).filter((GameEntry.game_date == hitter.game_date) &
                                                          ((GameEntry.away_team == hitter.hitter_entry.team) |
                                                           (GameEntry.home_team == hitter.hitter_entry.team)))
    print game_entry.count()
    if game_entry.count() == 1:
        print "%s going to %s" % (hitter.game_time, game_entry[0].game_time)
        hitter.game_time = game_entry[0].game_time
        #hitter.game_time = "12:00:00:34"
        hitter.game_date = game_entry[0].game_date
        if hitter.team == game_entry[0].away_team:
            hitter.opposing_team = game_entry[0].home_team
        else:
            hitter.opposing_team = game_entry[0].away_team
database_session.commit()
"""