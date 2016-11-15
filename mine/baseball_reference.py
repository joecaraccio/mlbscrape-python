
from beautiful_soup_helper import *
from datetime import date, timedelta
import bidict


class TeamInformation(object):
    def __init__(self, team_abbreviation, hitter_factor, pitcher_factor):
        self.team_abbreviation = team_abbreviation
        self.hitter_factor = hitter_factor
        self.pitcher_factor = pitcher_factor

BASE_URL = "http://www.baseball-reference.com"


def url_to_year(url):
    date_members = url.split("/")
    date_object = date_members[len(date_members)-2]

    return int(date_object.split("_")[1])


def get_pitcher_hand(boxscore_soup, players_soup, team_string):
    pitch_fx_id = boxscore_soup.find("pitching", {"team_flag": team_string}).find("pitcher").get("id")
    return players_soup.find("player", {"id": pitch_fx_id}).get("rl")


class HandEnum(object):
    LHP = 1
    RHP = 2


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
        soup = get_hitter_soup(year)

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

    raise NameNotFound(full_name)


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
        soup = get_pitcher_soup(year)

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

    raise NameNotFound(full_name)


class NameNotFound(Exception):
    def __init__(self, name_str):
        super(NameNotFound, self).__init__("Player '%s' not found in the Baseball Reference page" % name_str)


def get_hitter_soup(year=None):
    if year is None:
        year = date.today().year

    hitter_year_url = BASE_URL + "/leagues/MLB/" + str(year) + "-standard-batting.shtml"
    return get_soup_from_url(hitter_year_url)


def get_pitcher_soup(year=None):
    if year is None:
        year = date.today().year

    pitcher_year_url = BASE_URL + "/leagues/MLB/" + str(year) + "-standard-pitching.shtml"
    return get_soup_from_url(pitcher_year_url)


class TableNotFound(Exception):
    def __init__(self, table_name):
        super(TableNotFound, self).__init__("Table '%s' not found in the Baseball Reference page" % table_name)


class TableRowNotFound(Exception):
    def __init__(self, table_row, table_column, table_name):
        super(TableRowNotFound, self).__init__("Table row '%s' not found in the column '%s' in the "
                                               "table %s in the Baseball Reference page" %
                                               (table_row, table_column, table_name))


class DidNotFacePitcher(Exception):
    def __init__(self, hitter_name, pitcher_name):
        super(DidNotFacePitcher, self).__init__("Player %s has never faced pitcher %s" % hitter_name, pitcher_name)


def get_vs_table_row_dict(soup, batter_id, pitcher_id):
    """ Special version of get_table_row_dict. Since Baseball Reference's batter vs. pitcher
    tables don't really have a standardized row name, we have to just count the number of rows and
    accumulate the stats.
    :param soup: BeautifulSoup object containing the table HTML
    :param batter_id: the Baseball Reference ID of the relevant batter
    :param pitcher_id: the Baseball Reference ID of the relevant pitcher
    :return: a dictionary representing the stats
    """
    # TODO: we may not need the base url outside of unit tests
    batter_vs_pitcher_base = BASE_URL + "/play-index/batter_vs_pitcher.cgi?batter="

    results_table = soup.find("table", {"id": "ajax_result_table"})
    if results_table is None:
        raise TableNotFound("ajax_result_table")

    table_header_list = results_table.find("thead").findAll("th")
    table_header_list = [x.text for x in table_header_list]
    table_body = results_table.find("tbody")

    matching_url = batter_vs_pitcher_base + batter_id + "&pitcher=" + pitcher_id
    try:
        stat_row = table_body.find("a", {"href": matching_url}).parent.parent
    except AttributeError:
        raise TableRowNotFound(matching_url, "NULL", "ajax_result_table")

    # Create a dictionary of the stat attributes
    stat_dict = dict()
    stat_entries = stat_row.findAll("td")
    # The dictionary does not have valid entries, move on to the next row
    if len(stat_entries) != len(table_header_list):
        raise TableRowNotFound(matching_url, "NULL", "ajax_result_table")
    for i in range(0, len(table_header_list)):
        if stat_entries[i].text == "":
            stat_dict[table_header_list[i]] = 0
        else:
            stat_dict[table_header_list[i]] = stat_entries[i].text.replace(u"\xa0", " ")

    return stat_dict


def get_table_row_dict(soup, table_name, table_row_label, table_column_label):
    results_table = soup.find("table", {"id": table_name})
    if results_table is None:
        raise TableNotFound(table_name)

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

    raise TableRowNotFound(table_row_label, table_column_label, table_name)


def get_career_hitting_stats(baseball_reference_id, soup=None):
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/split.cgi?id=" +
                                                     str(baseball_reference_id) + "&year=Career&t=b")

    return get_table_row_dict(soup, "total", "Career Totals", "Split")


def get_vs_hand_hitting_stats(baseball_reference_id, hand_value, soup=None):
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/split.cgi?id=" +
                                                     str(baseball_reference_id) + "&year=Career&t=b")

    if hand_value is HandEnum.LHP:
        hand = "vs LHP"
    elif hand_value is HandEnum.RHP:
        hand = "vs RHP"
    else:
        print "Invalid hand enum."
        return None

    return get_table_row_dict(soup, "plato", hand, "Split")


def get_recent_hitting_stats(baseball_reference_id, soup=None):
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/split.cgi?id=" +
                                                     str(baseball_reference_id) + "&year=Career&t=b")

    return get_table_row_dict(soup, "total", "Last 7 days", "Split")


def get_season_hitting_stats(baseball_reference_id, year=None, soup=None):
    if year is None:
        year = date.today().year
    if soup is None:
        url = BASE_URL + "/players/split.cgi?id=" + str(baseball_reference_id) + "&year=" + \
              str(year) + "&t=b"
        print url
        soup = get_soup_from_url(url)

    return get_table_row_dict(soup, "total", str(year) + " Totals", "Split")


def get_vs_pitcher_stats(batter_id, pitcher_id, soup=None):
    if soup is None:
        url = BASE_URL + "/play-index/batter_vs_pitcher.cgi?batter=" + str(batter_id)
        print url
        soup = get_soup_from_url(url)

    return get_vs_table_row_dict(soup, batter_id, pitcher_id)


def get_hitter_page_career_soup(baseball_reference_id):
    return get_soup_from_url(BASE_URL + "/players/split.cgi?id=" +
                                                 str(baseball_reference_id) + "&year=Career&t=b")


def get_career_pitching_stats(baseball_reference_id, soup=None):
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/split.cgi?id=" +
                                                     str(baseball_reference_id) + "&year=Career&t=p")

    return get_table_row_dict(soup, "total_extra", "Career Totals", "Split")


def get_pitcher_page_career_soup(baseball_reference_id):
    url = BASE_URL + "/players/split.cgi?id=" + str(baseball_reference_id) + "&year=Career&t=p"
    print url
    return get_soup_from_url(url)


def get_season_pitcher_stats(baseball_reference_id, year=None, soup=None):
    if year is None:
        year = date.today().year
    if soup is None:
        url = BASE_URL + "/players/split.cgi?id=" + str(baseball_reference_id) + "&year=" + \
              str(year) + "&t=p"
        print url
        soup = get_soup_from_url(url)

    return get_table_row_dict(soup, "total_extra", str(year) + " Totals", "Split")


def get_recent_pitcher_stats(baseball_reference_id, soup=None):
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/split.cgi?id=" +
                                                     str(baseball_reference_id) + "&year=Career&t=p")

    return get_table_row_dict(soup, "total_extra", "Last 14 days", "Split")


def get_yesterdays_hitting_game_log(baseball_reference_id, soup=None):
    yesterdays_date = date.today() - timedelta(days=1)
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/gl.cgi?id=" +
                                                     str(baseball_reference_id) + "&t=b&year=" +
                                                     str(yesterdays_date.year))
    try:
        return get_table_row_dict(soup, "batting_gamelogs", date_abbreviations[yesterdays_date.month] + " " +
                                  str(yesterdays_date.day), "Date")
    # TODO: just try again for now, explore BeautifulSoup built-in options for this
    except TableNotFound as e:
        print e
        return get_table_row_dict(soup, "batting_gamelogs", date_abbreviations[yesterdays_date.month] + " " +
                                  str(yesterdays_date.day), "Date")


def get_pitching_game_log(baseball_reference_id, soup=None, game_date=None):
    if game_date is None:
        game_date = date.today() - timedelta(days=1)
    if soup is None:
        soup = get_soup_from_url(BASE_URL + "/players/gl.cgi?id=" +
                                                     str(baseball_reference_id) + "&t=p&year=" + str(game_date.year))
    return get_table_row_dict(soup, "pitching_gamelogs", date_abbreviations[game_date.month] + " " +
                              str(game_date.day), "Date")


def get_team_info(team_name, year_of_interest=None, team_soup=None):
    url = "/about/parkadjust.shtml"

    team_abbreviation = team_dict.inv[team_name]

    if year_of_interest is None:
        year_of_interest = date.today().year

    if team_soup is None:
        team_soup = get_soup_from_url(BASE_URL + "/teams/" +
                                                          team_abbreviation + "/" + str(year_of_interest) + ".shtml")

    sub_nodes = team_soup.find("a", {"href": url}).parent.parent.findAll("strong")
    for sub_node in sub_nodes:
        for content in sub_node.contents:
            if "multi-year:" in content:
                factor_string = sub_node.next_sibling.split(",")

                hitter_factor = int(factor_string[0].split("-")[1].strip().split(" ")[0])
                pitcher_factor = int(factor_string[1].split("-")[1].strip().split(" ")[0])

                return hitter_factor, pitcher_factor

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
