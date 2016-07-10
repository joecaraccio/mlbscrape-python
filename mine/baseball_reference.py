
from beautiful_soup_helper import BeautifulSoupHelper
import bisect
from datetime import date, timedelta
import bidict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TeamInformation(object):
    def __init__(self, team_abbreviation, hitter_factor, pitcher_factor):
        self.team_abbreviation = team_abbreviation
        self.hitter_factor = hitter_factor
        self.pitcher_factor = pitcher_factor

class BaseballReference(object):
    BASE_URL = "http://www.baseball-reference.com"

    @staticmethod
    def url_to_year(url):
        date_members = url.split("/")
        date_object = date_members[len(date_members)-2]

        return int(date_object.split("_")[1])

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


    class HandEnum():
        LHP = 1
        RHP = 2

    @staticmethod
    def get_hitter_id(full_name, team, year=None, soup=None):
        """ Get the BaseballReference ID from the players name and team
        :param full_name: the full name of the player
        :param team: the BaseballReference team abbreviation
        :param year: an integer representing the year of interest (this is particularly useful because players may
        change teams (if None, the method will use the current year)
        :param soup: BeautifulSoup object of all players in the given year
        :return: string representation of the player's ID
        """

        if year is None:
            year = date.today().year

        if soup is None:
            soup = BaseballReference.get_hitter_soup(year)

        hitter_table = soup.find("table", {"id": "players_standard_batting"}).find("tbody")
        hitter_table_rows = hitter_table.findAll("tr")
        for hitter_table_row in hitter_table_rows:
            if hitter_table_row.get("class")[0] != "thead":
                try:
                    hitter_entries = hitter_table_row.findAll("td")
                    hitter_name_entry = hitter_entries[1].find("a")
                    if hitter_name_entry.text.replace(u'\xa0', ' ') == full_name:
                        if team == hitter_entries[3].text:
                            hitter_id = hitter_name_entry.get("href").split("/")
                            return str(hitter_id[len(hitter_id)-1]).replace(".shtml", "")
                except IndexError:
                    continue
                except AttributeError:
                    continue

        raise BaseballReference.NameNotFound(full_name)

    @staticmethod
    def get_pitcher_id(full_name, team, year=None, soup=None):
        """ Get the BaseballReference ID from the players name and team
        :param full_name: the full name of the player
        :param team: the BaseballReference team abbreviation
        :param year: an integer representing the year of interest (this is particularly useful because players may
        change teams (if None, the method will use the current year)
        :param soup: BeautifulSoup object of all players in the given year
        :return: string representation of the player's ID
        """

        if year is None:
            year = date.today().year

        if soup is None:
            soup = BaseballReference.get_pitcher_soup(year)

        pitcher_table = soup.find("table", {"id": "players_standard_pitching"}).find("tbody")
        pitcher_table_rows = pitcher_table.findAll("tr")
        for pitcher_table_row in pitcher_table_rows:
            if pitcher_table_row.get("class")[0] != "thead":
                try:
                    pitcher_entries = pitcher_table_row.findAll("td")
                    pitcher_name_entry = pitcher_entries[1].find("a")
                    if pitcher_name_entry.text.replace(u'\xa0', ' ') == full_name:
                        if team == pitcher_entries[3].text:
                            pitcher_id = pitcher_name_entry.get("href").split("/")
                            return str(pitcher_id[len(pitcher_id)-1]).replace(".shtml", "")
                except IndexError:
                    continue
                except AttributeError:
                    continue

        raise BaseballReference.NameNotFound(full_name)

    class NameNotFound(Exception):
        def __init__(self, name_str):
            super(BaseballReference.NameNotFound, self).__init__("Player '%s' not found in the Baseball Reference page" %
                                                                 name_str)

    @staticmethod
    def get_hitter_soup(year=None):
        if year is None:
            year = date.today().year

        hitter_year_url = BaseballReference.BASE_URL + "/leagues/MLB/" + str(year) + "-standard-batting.shtml"
        return BeautifulSoupHelper.get_soup_from_url(hitter_year_url)

    @staticmethod
    def get_pitcher_soup(year=None):
        if year is None:
            year = date.today().year

        pitcher_year_url = BaseballReference.BASE_URL + "/leagues/MLB/" + str(year) + "-standard-pitching.shtml"
        return BeautifulSoupHelper.get_soup_from_url(pitcher_year_url)

    class TableNotFound(Exception):
        def __init__(self, table_name):
            super(BaseballReference.TableNotFound, self).__init__("Table '%s' not found in the Baseball Reference page" %
                                                                  table_name)

    class TableRowNotFound(Exception):
        def __init__(self, table_row, table_column, table_name):
            super(BaseballReference.TableRowNotFound, self).__init__("Table row '%s' not found in the column '%s' in the"
                                                                     "table %s in the Baseball Reference page" %
                                                                     (table_row, table_column, table_name))

    @staticmethod
    def get_table_row_dict(soup, table_name, table_row_label, table_column_label):
        results_table = soup.find("table", {"id": table_name})
        if results_table is None:
            raise BaseballReference.TableNotFound(table_name)

        table_header_list = results_table.find("thead").findAll("th")
        table_header_list = [x.text for x in table_header_list]
        stat_rows = results_table.find("tbody").findAll("tr")

        for stat_row in stat_rows:
            # Create a dictionary of the stat attributes
            stat_dict = dict()
            stat_entries = stat_row.findAll("td")
            # The dictionary does not have valid entries, move on to the next row
            if len(stat_entries) != len(table_header_list):
                continue
            for i in range(0, len(table_header_list)):
                if stat_entries[i].text == "":
                    stat_dict[table_header_list[i]] = 0
                else:
                    stat_dict[table_header_list[i]] = stat_entries[i].text.replace(u"\xa0", " ")
            try:
                if stat_dict[table_column_label] == table_row_label:
                    return stat_dict
            # We have reached the end of the year-by-year stats, just end
            except ValueError:
                break

        raise BaseballReference.TableRowNotFound(table_row_label, table_column_label, table_name)

    @staticmethod
    def get_career_hitting_stats(baseball_reference_id, soup=None):
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/split.cgi?id=" +
                                                         str(baseball_reference_id) + "&year=Career&t=b")

        return BaseballReference.get_table_row_dict(soup, "total", "Career Totals", "Split")

    @staticmethod
    def get_vs_hand_hitting_stats(baseball_reference_id, hand_value, soup=None):
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/split.cgi?id=" +
                                                         str(baseball_reference_id) + "&year=Career&t=b")

        if hand_value is BaseballReference.HandEnum.LHP:
            hand = "vs LHP"
        elif hand_value is BaseballReference.HandEnum.RHP:
            hand = "vs RHP"
        else:
            print "Invalid hand enum."
            return None

        return BaseballReference.get_table_row_dict(soup, "plato", hand, "Split")

    @staticmethod
    def get_recent_hitting_stats(baseball_reference_id, soup=None):
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/split.cgi?id=" +
                                                         str(baseball_reference_id) + "&year=Career&t=b")

        return BaseballReference.get_table_row_dict(soup, "total", "Last 7 days", "Split")

    @staticmethod
    def get_season_hitting_stats(baseball_reference_id, year=None, soup=None):
        if year is None:
            year = date.today().year
        if soup is None:
            url = BaseballReference.BASE_URL + "/players/split.cgi?id=" + str(baseball_reference_id) + "&year=" + \
                  str(year) + "&t=b"
            print url
            soup = BeautifulSoupHelper.get_soup_from_url(url)

        return BaseballReference.get_table_row_dict(soup, "total", str(year) + " Totals", "Split")

    @staticmethod
    def get_vs_pitcher_stats(batter_id, pitcher_id, soup=None):
        if soup is None:
            url = BaseballReference.BASE_URL + "/play-index/batter_vs_pitcher.cgi?batter=" + str(batter_id) + \
                  "&pitcher=" + str(pitcher_id)
            print url
            soup = BeautifulSoupHelper.get_soup_from_url(url)

        return BaseballReference.get_table_row_dict(soup, "ajax_result_table_1", "RegSeason", "Year")

    @staticmethod
    def get_hitter_page_career_soup(baseball_reference_id):
        return BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/split.cgi?id=" +
                                                     str(baseball_reference_id) + "&year=Career&t=b")

    @staticmethod
    def get_career_pitching_stats(baseball_reference_id, soup=None):
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/split.cgi?id=" +
                                                         str(baseball_reference_id) + "&year=Career&t=p")

        return BaseballReference.get_table_row_dict(soup, "total_extra", "Career Totals", "Split")

    @staticmethod
    def get_pitcher_page_career_soup(baseball_reference_id):
        url = BaseballReference.BASE_URL + "/players/split.cgi?id=" + str(baseball_reference_id) + "&year=Career&t=p"
        print url
        return BeautifulSoupHelper.get_soup_from_url(url)

    @staticmethod
    def get_season_pitcher_stats(baseball_reference_id, year=None, soup=None):
        if year is None:
            year = date.today().year
        if soup is None:
            url = BaseballReference.BASE_URL + "/players/split.cgi?id=" + str(baseball_reference_id) + "&year=" + \
                  str(year) + "&t=p"
            print url
            soup = BeautifulSoupHelper.get_soup_from_url(url)

        return BaseballReference.get_table_row_dict(soup, "total_extra", str(year) + " Totals", "Split")

    @staticmethod
    def get_recent_pitcher_stats(baseball_reference_id, soup=None):
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/split.cgi?id=" +
                                                         str(baseball_reference_id) + "&year=Career&t=p")

        return BaseballReference.get_table_row_dict(soup, "total_extra", "Last 14 days", "Split")

    @staticmethod
    def get_yesterdays_hitting_game_log(baseball_reference_id, soup=None):
        yesterdays_date = date.today() - timedelta(days=1)
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/gl.cgi?id=" +
                                                         str(baseball_reference_id) + "&t=b&year=" + str(yesterdays_date.year))
        return BaseballReference.get_table_row_dict(soup, "batting_gamelogs",
                                                    BaseballReference.date_abbreviations[yesterdays_date.month] + " " + str(yesterdays_date.day),
                                                    "Date")

    @staticmethod
    def get_pitching_game_log(baseball_reference_id, soup=None, game_date=None):
        if game_date is None:
            game_date = date.today() - timedelta(days=1)
        if soup is None:
            soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/players/gl.cgi?id=" +
                                                         str(baseball_reference_id) + "&t=p&year=" + str(game_date.year))
        return BaseballReference.get_table_row_dict(soup, "pitching_gamelogs",
                                                    BaseballReference.date_abbreviations[game_date.month] + " " + str(game_date.day),
                                                    "Date")

    @staticmethod
    def get_team_info(team_name, year_of_interest=None, team_soup=None):
        URL = "/about/parkadjust.shtml"
        try:
            team_abbreviation = BaseballReference.team_dict.inv[team_name]
        except KeyError:
            raise BaseballReference.InvalidTeamName(team_name)

        if year_of_interest is None:
            year_of_interest = date.today().year

        if team_soup is None:
            team_soup = BeautifulSoupHelper.get_soup_from_url(BaseballReference.BASE_URL + "/teams/" +
                                                          team_abbreviation + "/" + year_of_interest + ".shtml")

        sub_nodes = team_soup.find("a", {"href": URL}).parent.parent.findAll("strong")
        for sub_node in sub_nodes:
            for content in sub_node.contents:
                if "multi-year:" in content:
                    factor_string = sub_node.next_sibling.split(",")

                    hitter_factor = int(factor_string[0].split("-")[1].strip().split(" ")[0])
                    pitcher_factor = int(factor_string[1].split("-")[1].strip().split(" ")[0])

                    return TeamInformation(team_abbreviation, hitter_factor, pitcher_factor)

        return None

    # Two-way dictionary
    team_dict = bidict.bidict(ARI="Arizona Diamondbacks",
                              ATL="Atlanta Braves",
                              BAL="Baltimore Orioles",
                              BOS="Boston Red Sox",
                              CHC="Chicago Cubs",
                              CHW="Chicago White Sox",
                              CIN="Cincinnati Reds",
                              CLE="Cleveland Indians",
                              COL="Colorado Rockies",
                              DET="Detroit Tigers",
                              HOU="Houston Astros",
                              KCR="Kansas City Royals",
                              LAA="Los Angeles Angels",
                              LAD="Los Angeles Dodgers",
                              MIA="Miami Marlins",
                              MIL="Milwaukee Brewers",
                              MIN="Minnesota Twins",
                              NYM="New York Mets",
                              NYY="New York Yankees",
                              OAK="Oakland Athletics",
                              PHI="Philadelphia Phillies",
                              PIT="Pittsburgh Pirates",
                              SDP="San Diego Padres",
                              SEA="Seattle Mariners",
                              SFG="San Francisco Giants",
                              STL="St. Louis Cardinals",
                              TBR="Tampa Bay Rays",
                              TEX="Texas Rangers",
                              TOR="Toronto Blue Jays",
                              WSN="Washington Nationals")

    date_abbreviations = {1: "Jan",
                          2: "Feb",
                          3: "Mar",
                          4: "Apr",
                          5: "May",
                          6: "Jun",
                          7: "Jul",
                          8: "Aug",
                          9: "Sep",
                          10: "Oct",
                          11: "Nov",
                          12: "Dec"}
