
from beautiful_soup_helper import BeautifulSoupHelper
import bisect
from sortedcontainers import SortedList, SortedListWithKey
from hitter import Hitter

class PlayerSortedList(SortedListWithKey):
    def find_from_pitchfx(self, first_name, last_name, team):
        index = self.bisect_left(BaseballReference.PlayerStruct(first_name, last_name, None, None))
        if self[index].first_name != first_name or self[index].last_name != last_name:
            print "The player %s %s from team %s could not be identified in the Baseball Reference list." % (first_name,
                                                                                                             last_name,
                                                                                                             team)
            return None
        while self[index].team != BaseballReference.pitchfx_team_to_team[team.upper()]:
            index += 1
            if index >= len(self) or self[index].first_name != first_name or self[index].last_name != last_name:
                print "The player %s %s from team %s could not be identified in the Baseball Reference list." % \
                      (first_name, last_name, team)
                return None

        return self[index]


class BaseballReference(object):
    BASE_URL = "http://www.baseball-reference.com"

    @staticmethod
    def url_to_year(url):
        date_members = url.split("/")
        date_object = date_members[len(date_members)-2]

        return int(date_object.split("_")[1])

    class PlayerStruct(object):
        def __init__(self, first_name, last_name, reference_id, team):
            self.first_name = first_name
            self.last_name = last_name
            self.baseball_reference_id = reference_id
            self.team = team

    class BatterStatStruct(object):
        def __init__(self, ab=None, h=None, bb=None, so=None, hr=None, rbi=None, runs=None, sb=None, cs=None):
            self.ab = 0
            self.h = 0
            self.bb = 0
            self.so = 0
            self.hr = 0
            self.rbi = 0
            self.r = 0
            self.sb = 0
            self.cs = 0
            if ab is not None:
                self.ab = ab
            if h is not None:
                self.h = h
            if bb is not None:
                self.bb = bb
            if so is not None:
                self.so = so
            if hr is not None:
                self.hr = hr
            if rbi is not None:
                self.rbi = rbi
            if runs is not None:
                self.r = runs
            if sb is not None:
                self.sb = sb
            if cs is not None:
                self.cs = cs

    @staticmethod
    def get_pitcher_id(boxscore_soup, players_soup, team_string, pitchers_set):
        full_name = boxscore_soup.find("pitching", {"team_flag": team_string}).find("pitcher").get("name_display_first_last")
        full_name = full_name.split(" ")
        first_name = full_name[0]
        last_name = " ".join(str(x) for x in full_name[1:len(full_name)])
        team = players_soup.find("team", {"type":team_string}).get("id")
        return pitchers_set.find_from_pitchfx(first_name, last_name, team).baseball_reference_id

    @staticmethod
    def get_pitcher_hand(boxscore_soup, players_soup, team_string):
        pitch_fx_id = boxscore_soup.find("pitching", {"team_flag": team_string}).find("pitcher").get("id")
        return players_soup.find("player", {"id": pitch_fx_id}).get("rl")

    @staticmethod
    def get_id_from_url(url):
        """ Extract the unique Baseball Reference ID for this player
        Note: the typical relative URL is "/players/[last name letter]/[player ID].shtml"
        :param url: relative URL to the player's Baseball Reference page from the base URL
        :return: string representation of the Baseball Reference ID
        """
        end_url = url.split("/")
        end_url = end_url[len(end_url)-1]
        return end_url.split(".")[0]

    @staticmethod
    def get_player_set_from_year(year, url, table_name):
        """ Get a dictionary of players from the
        :param year: integer representation of the year
        :return: Dictionary of player structs
        """
        player_year_soup = BeautifulSoupHelper.get_soup_from_url(url)
        player_table = player_year_soup.find("table", {"id": table_name})
        """ Note: using a SortedList is to be safe. Given BaseballReference's current page, it is already in
        alphabetical order.
        """
        player_set = PlayerSortedList(key=lambda r: r.first_name + " " + r.last_name)
        if player_table is None:
            print "The player table for year " + str(year) + " could not be found. Check the URL: " + url
            return player_set

        player_table_body = player_table.find("tbody")
        for player in player_table_body.findAll("tr"):

            # Filter out headers and the table totals
            if "thead" in player.get("class") or "league_average_table" in player.get("class"):
                continue

            table_entries = player.findAll("td")

            # Get the first and last name of the batter
            try:
                name = table_entries[1].find("a").text
            except IndexError:
                print "Player Set: The player %s does not have enough entries in the table." % player
                assert 0
            name = name.split()
            try:
                first_name = name[0]
                last_name = " ".join(str(x) for x in name[1:len(name)])
            except IndexError:
                print "Player Set: The player % does not contain a space between first and last name." % player
                assert 0

            # Get the URL for the batter in the table
            try:
                player_url = table_entries[1].find("a").get("href")
            except IndexError:
                print "Player Set: The player %s %s does not have enough entries to provide the URL for the player." %\
                      (first_name, last_name)
                assert 0
            try:
                team = table_entries[3].find("a").text
            except IndexError:
                print "Player Set: The player %s %s does not have enough entries to provide the team for the player." %\
                      (first_name, last_name)
            except AttributeError:
                print "Player Set Warning: The player %s %s played for both leagues in the year." % (first_name, last_name)
            player = BaseballReference.PlayerStruct(first_name, last_name,
                                                    BaseballReference.get_id_from_url(player_url),
                                                    team)
            player_set.add(player)

        print len(player_set)
        return player_set

    @staticmethod
    def get_batter_set_from_year(year):
        batter_url = BaseballReference.BASE_URL + "/leagues/MLB/" + str(year) + "-standard-batting.shtml"
        return BaseballReference.get_player_set_from_year(year, batter_url, "players_standard_batting")

    @staticmethod
    def get_pitcher_set_from_year(year):
        pitcher_url = BaseballReference.BASE_URL + "/leagues/MLB/" + str(year) + "-standard-pitching.shtml"
        return BaseballReference.get_player_set_from_year(year, pitcher_url, "players_standard_pitching")

    @staticmethod
    def get_vs_pitcher_stats_by_year(batter_id, pitcher_id, year):
        vs_url = BaseballReference.BASE_URL + "/play-index/batter_vs_pitcher.cgi?batter=" + batter_id + "&pitcher=" + \
                 pitcher_id
        batter_soup = BeautifulSoupHelper.get_soup_from_url(vs_url)
        if batter_soup is not None:
            results_table = batter_soup.find("table", {"id": "ajax_result_table_1"})
            table_header_list = results_table.find("thead").findAll("th")
            table_header_list = [x.text for x in table_header_list]
            year_entries = results_table.find("tbody").findAll("tr")
            stats = BaseballReference.BatterStatStruct()
            for year_entry in year_entries:
                # Create a dictionary of the stat attributes
                year_stat_dict = dict()
                year_stats = year_entry.findAll("td")
                for i in range(1, len(table_header_list)):
                    year_stat_dict[table_header_list[i]] = year_stats[i].text
                try:
                    if int(year_stat_dict["Year"]) >= year:
                        break
                # We have reached the end of the year-by-year stats, just end
                except ValueError:
                    break
                stats.ab += int(year_stat_dict["AB"])
                stats.h += int(year_stat_dict["H"])
                stats.bb += int(year_stat_dict["BB"])
                stats.so += int(year_stat_dict["SO"])
                stats.hr += int(year_stat_dict["HR"])
                stats.rbi += int(year_stat_dict["RBI"])

            return stats

    class HandEnum:
        LHP = 1
        RHP = 2

    @staticmethod
    def get_vs_stats_by_year(batter_id, hand, year):
        if hand is BaseballReference.HandEnum.LHP:
            vs_url = BaseballReference.BASE_URL + "/play-index/split_stats.cgi?full=1&params=plato|vs LHP|" + batter_id + \
                     "|bat|"
            results_id_tag = "vs_LHP1"
        else:
            vs_url = BaseballReference.BASE_URL + "/play-index/split_stats.cgi?full=1&params=plato|vs RHP|" + batter_id + \
                     "|bat|"
            results_id_tag = "vs_RHP1"
        batter_soup = BeautifulSoupHelper.get_soup_from_url(vs_url)
        if batter_soup is not None:
            results_table = batter_soup.find("table", {"id": results_id_tag})
            table_header_list = results_table.find("thead").findAll("th")
            table_header_list = [x.text for x in table_header_list]
            year_entries = results_table.find("tbody").findAll("tr")
            stats = BaseballReference.BatterStatStruct()
            for year_entry in year_entries:
                # Create a dictionary of the stat attributes
                year_stat_dict = dict()
                year_stats = year_entry.findAll("td")
                for i in range(1, len(table_header_list)):
                    if year_stats[i].text == "":
                        year_stat_dict[table_header_list[i]] = 0
                    else:
                        year_stat_dict[table_header_list[i]] = year_stats[i].text
                try:
                    if int(year_stat_dict["Year"]) >= year:
                        break
                # We have reached the end of the year-by-year stats, just end
                except ValueError:
                    break

                stats.ab += int(year_stat_dict["AB"])
                stats.h += int(year_stat_dict["H"])
                stats.bb += int(year_stat_dict["BB"])
                stats.so += int(year_stat_dict["SO"])
                stats.hr += int(year_stat_dict["HR"])
                stats.rbi += int(year_stat_dict["RBI"])
                stats.r += int(year_stat_dict["R"])
                stats.sb += int(year_stat_dict["SB"])
                stats.cs += int(year_stat_dict["CS"])

            return stats

    @staticmethod
    def build_hitter(batters_set, pitchers_set, player_soup, home_away_string, game_url, boxscore_soup, players_soup):
        """
        :param batters_set: a SortedListWithKey container containing all the batters from the relevant year
        :param pitchers_set: a SortedListWithKey container containing all the pitchers from the relevant year
        :param player_soup: BeautifulSoup object containing the XML info from players.xml
        :param home_away_string: "home" or "away" indicating
        :param game_url: the absolute URL of the game containing this batter
        :param boxscore_soup: BeautifulSoup object of boxscore.xml file
        :param players_soup: BeautifulSoup object of players.xml file
        :return: the resulting Hitter object
        """
        game_id = boxscore_soup.find("boxscore").get("game_id")
        baseball_reference_id = batters_set.find_from_pitchfx(player_soup.get("first"),
                                                              player_soup.get("last"),
                                                              player_soup.get("team_abbrev")).baseball_reference_id

        hitter = Hitter(player_soup.get("first"), player_soup.get("last"), player_soup.get("id"), baseball_reference_id,
                        player_soup.get("team_abbrev"), player_soup.get("bat_order"), player_soup.get("bats"))
        hitter.set_game_results(game_id, boxscore_soup.find("batter", {"id": player_soup.get("id")}))

        # Mine the pregame stats
        pregame_stats_soup = BeautifulSoupHelper.get_soup_from_url(game_url + "batters/" + player_soup.get("id") + ".xml")

        pitcher_id = BaseballReference.get_pitcher_id(boxscore_soup, players_soup, home_away_string,
                                                      pitchers_set)
        hitter.set_season_stats(pregame_stats_soup)
        hitter.set_career_stats(pregame_stats_soup)
        hitter.set_month_stats(pregame_stats_soup)
        year = BaseballReference.url_to_year(game_url)
        vs_stats = BaseballReference.get_vs_pitcher_stats_by_year(baseball_reference_id, pitcher_id, year)
        pitcher_hand = BaseballReference.get_pitcher_hand(boxscore_soup, players_soup, home_away_string)
        if pitcher_hand == "L":
            vs_hand_stats = BaseballReference.get_vs_stats_by_year(baseball_reference_id, BaseballReference.HandEnum.LHP,
                                                                  year)
        else:
            vs_hand_stats = BaseballReference.get_vs_stats_by_year(baseball_reference_id, BaseballReference.HandEnum.RHP,
                                                                   year)
        hitter.set_vs_stats(vs_stats, vs_hand_stats, year)

        return hitter

    pitchfx_team_to_team = {"ARI": "ARI",
                            "ATL": "ATL",
                            "BAL": "BAL",
                            "BOS": "BOS",
                            "CHC": "CHC",
                            "CWS": "CHW",
                            "CIN": "CIN",
                            "CLE": "CLE",
                            "COL": "COL",
                            "DET": "DET",
                            "HOU": "HOU",
                            "KC": "KCR",
                            "LAA": "LAA",
                            "LAD": "LAD",
                            "MIA": "MIA",
                            "MIL": "MIL",
                            "MIN": "MIN",
                            "NYM": "NYM",
                            "NYY": "NYY",
                            "OAK": "OAK",
                            "PHI": "PHI",
                            "PIT": "PIT",
                            "SD": "SDP",
                            "SEA": "SEA",
                            "SF": "SFG",
                            "STL": "STL",
                            "TB": "TBR",
                            "TEX": "TEX",
                            "TOR": "TOR",
                            "WSH": "WSN"}