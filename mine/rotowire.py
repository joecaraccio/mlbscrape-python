from datetime import datetime
from sql.hitter_entry import HitterEntry
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.pitcher_entry import PitcherEntry
from sqlalchemy.exc import IntegrityError
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.mlb_database import MlbDatabase
from sql.game import GameEntry
from multiprocessing import Pool
from mine.draft_kings import get_hitter_points, get_pitcher_points
from mine.baseball_reference import *

# Daily lineups relevant HTML labels
DAILY_LINEUPS_URL = "http://www.rotowire.com/baseball/daily_lineups.htm"
GAME_REGION_LABEL = "offset1 span15"
TEAM_REGION_LABEL = "span15 dlineups-topbox"
AWAY_TEAM_REGION_LABEL = "span5 dlineups-topboxleft"
HOME_TEAM_REGION_LABEL = "span5 dlineups-topboxright"
TIME_REGION_LABEL = "dlineups-topboxcenter-topline"
AWAY_TEAM_PLAYER_LABEL = "dlineups-vplayer"
HOME_TEAM_PLAYER_LABEL = "dlineups-hplayer"
LINEUPS_CLASS_LABEL = "span15 dlineups-mainbox"
POSITION_CLASS_LABEL = "dlineups-pos"
PITCHERS_REGION_LABEL = "span11 dlineups-pitchers"
HAND_CLASS_LABEL = "dlineups-lr"
DRAFTKINGS_LINK_LABEL = "span15 dlineups-promo-bottom"

# Individual player page relevant HTML labels
PLAYER_PAGE_BASE_URL = "http://www.rotowire.com/baseball/player.htm?id="
PLAYER_PAGE_LABEL = "span16 mlb-player-nameteam"
PLAYER_PAGE_CAREER_BASE_URL = "http://www.rotowire.com/baseball/plcareer.htm?id="
YEAR_TABLE_LABEL = "basicstats"
TABLE_ENTRY_LABEL = "mlbstat-year"
RECENT_TABLE_LABEL = "gamelog"
BATTER_SPLIT_BASE_URL = "http://www.rotowire.com/baseball/battersplit.htm?id="

# Split stats relevent HTML labels
SPLIT_TABLE_LABEL = "tablesorter makesortable"

WIND_LABEL = "dlineups-topboxcenter-bottomline"


class PlayerStruct(object):
    def __init__(self, name, team, rotowire_id, position, hand):
        self.name = name
        self.team = team
        self.rotowire_id = rotowire_id
        self.position = position
        self.hand = hand

    def __eq__(self, other):
        return self.name == other.name and self.team == other.team and self.rotowire_id == other.rotowire_id and \
               self.position == other.position and self.hand == other.hand


class Game(object):
    def __init__(self, away_lineup, away_pitcher, home_lineup, home_pitcher):
        self.home_lineup = home_lineup
        self.away_lineup = away_lineup
        self.away_pitcher = away_pitcher
        self.home_pitcher = home_pitcher

    def is_valid(self):
        if len(self.away_lineup) != 9 or len(self.home_lineup) != 9:
            return False

        return True


class HomeAwayEnum(object):
    AWAY = 0
    HOME = 1


def mine_pregame_stats():
    """ Mine the hitter/pitcher stats and predict the outcomes and commit to the database session
    """
    games = get_game_lineups()
    update_ids(games)
    get_pregame_hitting_stats_wrapper(games)
    get_pregame_pitching_stats_wrapper(games)


def get_game_lineups(db_path=None, url=None):
    """ Mine the RotoWire daily lineups page and get the players' name, team, and RotoWire ID
    Commit the GameEntry objects to the database.
    :param db_path: the relative path to the database (default is None)
    :param url: the URL containing the daily lineups (default is None)
    :return: list of Game objects representing the lineups for the day
    """

    database_session = MlbDatabase(db_path).open_session()

    if url is None:
        url = DAILY_LINEUPS_URL

    """TODO: add feature to look if it's going to rain"""
    lineup_soup = get_soup_from_url(url)
    header_nodes = lineup_soup.findAll("div", {"class": TEAM_REGION_LABEL})
    games = list()
    for header_node in header_nodes:
        game_node = header_node.parent
        home_team_lineup = list()
        away_team_lineup = list()
        away_team_abbreviation = game_node.find("div", {"class": AWAY_TEAM_REGION_LABEL}).text.split()[0]
        home_team_abbreviation = game_node.find("div", {"class": HOME_TEAM_REGION_LABEL}).text.split()[0]
        game_main_soup = game_node.find("div", {"class": LINEUPS_CLASS_LABEL})

        for away_player in game_main_soup.findAll("div", {"class": AWAY_TEAM_PLAYER_LABEL}):
            away_team_lineup.append(get_hitter(away_player, away_team_abbreviation, database_session))
        for home_player in game_main_soup.findAll("div", {"class": HOME_TEAM_PLAYER_LABEL}):
            home_team_lineup.append(get_hitter(home_player, home_team_abbreviation, database_session))

        try:
            pitchers = game_node.find("div", PITCHERS_REGION_LABEL).findAll("div")
            away_team_pitcher = get_pitcher(pitchers[0], away_team_abbreviation, database_session)
            home_team_pitcher = get_pitcher(pitchers[1], home_team_abbreviation, database_session)
        # No pitchers present on page
        except AttributeError:
            print "Game between %s and %s is not valid." % (away_team_abbreviation, home_team_abbreviation)
            continue

        current_game = Game(away_team_lineup, away_team_pitcher, home_team_lineup, home_team_pitcher)

        # TODO: since they only release the ump data ~1 hour before the game, we'll have to make this robust later
        try:
            game_time = game_node.find("div", {"class": TIME_REGION_LABEL}).find("a").text.replace("ET", "").strip()
            game_time = datetime.strptime(game_time, '%I:%M %p').strftime("%H:%M")
            game_entry = GameEntry(date.today(), game_time, home_team_abbreviation, away_team_abbreviation)
            game_entry.wind_speed = get_wind_speed(game_node)
            game_entry.ump_ks_per_game = get_ump_ks_per_game(game_node)
            game_entry.ump_runs_per_game = get_ump_runs_per_game(game_node)
            game_entry.park_hitter_score, game_entry.park_pitcher_score = get_team_info(team_dict[home_team_abbreviation])

            database_session.add(game_entry)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            print "Warning: attempt to duplicate game entry: %s %s %s %s" % (str(home_team_abbreviation),
                                                                             str(away_team_abbreviation),
                                                                             str(game_entry.game_date),
                                                                             str(game_entry.game_time))
        except Exception as e:
            print e
            pass

        if current_game.is_valid():
            games.append(current_game)
        else:
            print "Game between %s and %s is not valid." % (away_team_abbreviation, home_team_abbreviation)

    database_session.close()

    return games


def get_id(soup):
    """ Get the RotoWire ID from a BeautifulSoup node
    :param soup: BeautifulSoup object of the player in the daily lineups page
    """
    return soup.find("a").get("href").split("id=")[1]


def get_hitter(soup, team, database_session=None):
    """ Get a PlayerStruct representing a hitter
    If a database session is not provided, open the player page to obtain the hitter info.
    Otherwise, look for the hitter in the database. If not found, open the player page to obtain the hitter info.
    :param soup: BeautifulSoup object of the hitter in the daily lineups page
    :param team: team abbreviation of the hitter
    :param database_session: SQLAlchemy database session (default is None)
    """
    rotowire_id = get_id(soup)
    if database_session is None:
        name = get_name_from_id(rotowire_id)
    else:
        hitter_entry = database_session.query(HitterEntry).get(rotowire_id)
        if hitter_entry is not None:
            name = "%s %s" % (hitter_entry.first_name, hitter_entry.last_name)
            hand = hitter_entry.batting_hand
        else:
            name = get_name_from_id(rotowire_id)
            hand = get_hand(soup)
    position = soup.find("div", {"class": POSITION_CLASS_LABEL}).text

    return PlayerStruct(name, team, rotowire_id, position, hand)


def get_pitcher(soup, team, database_session=None):
    """ Get a PlayerStruct representing a pitcher
    If a database session is not provided, open the player page to obtain the pitcher info.
    Otherwise, look for the pitcher in the database. If not found, open the player page to obtain the pitcher info.
    :param soup: BeautifulSoup object of the pitcher in the daily lineups page
    :param team: team abbreviation of the pitcher
    :param database_session: SQLAlchemy database session (default is None)
    """
    rotowire_id = get_id(soup)
    if database_session is None:
        name = get_name_from_id(rotowire_id)
    else:
        pitcher_entry = database_session.query(PitcherEntry).get(rotowire_id)
        if pitcher_entry is not None:
            name = "%s %s" % (pitcher_entry.first_name, pitcher_entry.last_name)
            hand = pitcher_entry.pitching_hand
        else:
            name = get_name_from_id(rotowire_id)
            hand = get_hand(soup)

    return PlayerStruct(name, team, rotowire_id, "P", hand)


def create_new_hitter_entry(player_struct, baseball_reference_id, database_session):
    name = player_struct.name.split()
    first_name = name[0]
    last_name = " ".join(str(x) for x in name[1:len(name)])
    entry = HitterEntry(first_name, last_name, player_struct.rotowire_id)
    entry.team = player_struct.team
    entry.batting_hand = player_struct.hand
    entry.baseball_reference_id = baseball_reference_id

    database_session.add(entry)
    database_session.commit()


def create_new_pitcher_entry(player_struct, baseball_reference_id, database_session):
    name = player_struct.name.split()
    first_name = name[0]
    last_name = " ".join(str(x) for x in name[1:len(name)])
    entry = PitcherEntry(first_name, last_name, player_struct.rotowire_id)
    entry.team = player_struct.team
    entry.pitching_hand = player_struct.hand
    entry.baseball_reference_id = baseball_reference_id

    database_session.add(entry)
    database_session.commit()


def get_hand(soup):
    """
    :param soup: BeautifulSoup node of the player
    :return: Hand of the player
    """
    return soup.find("span", {"class": HAND_CLASS_LABEL}).text.strip().replace("(", "").replace(")", "")


def update_lineup_ids(lineup):
    database_session = MlbDatabase().open_session()

    hitter_soup = get_hitter_soup()
    for current_player in lineup:
        name = current_player.name.split()
        first_name = name[0]
        last_name = " ".join(str(x) for x in name[1:len(name)])
        db_query = database_session.query(HitterEntry).get(current_player.rotowire_id)
        # Found unique entry, check to make sure the team matches the database
        if db_query is not None:
            if db_query.team == current_player.team:
                continue
            # Update the player's team in the database
            else:
                db_query.team = current_player.team
                database_session.commit()
        # Found no entries, create a bare bones entry with just the name and id
        else:
            try:
                baseball_reference_id = get_hitter_id(first_name + " " + last_name,
                                                                        team_dict.inv[team_dict[current_player.team]],
                                                                        date.today().year,
                                                                        hitter_soup)
            except NameNotFound:
                print "Skipping committing this hitter '%s %s'." % (first_name, last_name)
                continue

            create_new_hitter_entry(current_player, baseball_reference_id, database_session)

    database_session.close()


def update_pitcher_id(pitcher):

    database_session = MlbDatabase().open_session()

    pitcher_soup = get_pitcher_soup()
    name = pitcher.name.split()
    first_name = name[0]
    last_name = " ".join(str(x) for x in name[1:len(name)])
    db_query = database_session.query(PitcherEntry).get(pitcher.rotowire_id)
    # Found unique entry, check to make sure the team matches the database
    if db_query is not None:
        if db_query.team == pitcher.team:
            return
        # Update the player's team in the database
        else:
            db_query.team = pitcher.team
            database_session.commit()
    # Found no entries, create a bare bones entry with just the name and id
    else:
        try:
            baseball_reference_id = get_pitcher_id(first_name + " " + last_name,
                                                                     team_dict.inv[team_dict[pitcher.team]],
                                                                     date.today().year,
                                                                     pitcher_soup)
        except NameNotFound:
            print "Skipping committing this pitcher '%s %s'." % (first_name, last_name)
            return

        create_new_pitcher_entry(pitcher, baseball_reference_id, database_session)

    database_session.close()


def update_ids(games):
    """ Check if each player is represented in the database. If not, commit a new entry
    :param games: list of Game objects
    """
    for game in games:
        update_lineup_ids(game.away_lineup)
        update_pitcher_id(game.away_pitcher)
        update_lineup_ids(game.home_lineup)
        update_pitcher_id(game.home_pitcher)


def get_name_from_id(rotowire_id):
    """ Use the acquired RotoWire ID to resolve the name in case it is too long for the
    daily lineups page.
    :param rotowire_id: unique ID for a player in RotoWire
    :return: str representation of the name of the player
    """
    player_soup = get_soup_from_url(PLAYER_PAGE_BASE_URL + str(rotowire_id))
    return player_soup.find("div", {"class": PLAYER_PAGE_LABEL}).find("h1").text.strip()


def get_pregame_hitting_stats(game):
    """ Mine pregame stats for all hitters in a given game and commit them to the database.
    :param game: Game struct containing the lineups
    """
    database_session = MlbDatabase().open_session()
    for current_hitter in game.away_lineup:
        pitcher_hand = game.home_pitcher.hand
        print "Mining %s." % current_hitter.name
        try:
            pregame_hitter_entry = get_hitter_stats(current_hitter.rotowire_id,
                                                    game.home_pitcher.rotowire_id,
                                                    current_hitter.team,
                                                    pitcher_hand,
                                                    database_session)
            pregame_hitter_entry.game_date = date.today()
            pregame_hitter_entry.opposing_team = game.home_pitcher.team
            database_session.add(pregame_hitter_entry)
            database_session.commit()
        except HitterNotFound as e:
            print e
        except IntegrityError:
            print "Attempt to duplicate hitter entry: %s %s %s" % (current_hitter.name,
                                                                   pregame_hitter_entry.team,
                                                                   pregame_hitter_entry.opposing_team)
            database_session.rollback()

    for current_hitter in game.home_lineup:
        pitcher_hand = game.away_pitcher.hand
        print "Mining %s." % current_hitter.name
        try:
            pregame_hitter_entry = get_hitter_stats(current_hitter.rotowire_id,
                                                             game.away_pitcher.rotowire_id,
                                                             current_hitter.team,
                                                             pitcher_hand,
                                                             database_session)
            pregame_hitter_entry.game_date = date.today()
            pregame_hitter_entry.opposing_team = game.away_pitcher.team
            database_session.add(pregame_hitter_entry)
            database_session.commit()
        except HitterNotFound as e:
            print e
        except IntegrityError:
            print "Attempt to duplicate hitter entry: %s %s %s" % (current_hitter.name,
                                                                   pregame_hitter_entry.team,
                                                                   pregame_hitter_entry.opposing_team)
            database_session.rollback()

    database_session.close()


def get_pregame_hitting_stats_wrapper(games):
    """ Organize a thread pool to mine the hitting stats in parallel
    :param games: list of Game structs containing the lineups
    """
    thread_pool = Pool(6)

    thread_pool.map(get_pregame_hitting_stats, games)


def get_pregame_pitching_stats_wrapper(games):
    """ Organize a thread pool to mine the pitching stats in parallel
    :param games: list of Game structs containing the pitchers
    """
    thread_pool = Pool(6)

    thread_pool.map(get_pregame_pitching_stats, games)


def get_pregame_pitching_stats(game):
    """ Mine pregame stats for both pitchers in a given game and commit them to the database.
    :param game: Game struct containing the pitchers
    """
    database_session = MlbDatabase().open_session()

    current_pitcher = game.away_pitcher
    print "Mining %s." % current_pitcher.name
    try:
        pregame_pitcher_entry = get_pitcher_stats(current_pitcher.rotowire_id,
                                                  current_pitcher.team,
                                                  game.home_pitcher.team,
                                                  database_session)

        database_session.add(pregame_pitcher_entry)
        database_session.commit()
    except IntegrityError:
        print "Attempt to duplicate pitcher entry: %s %s %s" % (current_pitcher.name,
                                                                pregame_pitcher_entry.team,
                                                                pregame_pitcher_entry.opposing_team)
        database_session.rollback()
    except PitcherNotFound as e:
        print e

    current_pitcher = game.home_pitcher
    print "Mining %s." % current_pitcher.name
    try:
        pregame_pitcher_entry = get_pitcher_stats(current_pitcher.rotowire_id,
                                                  current_pitcher.team,
                                                  game.away_pitcher.team,
                                                  database_session)

        database_session.add(pregame_pitcher_entry)
        database_session.commit()
    except IntegrityError:
        print "Attempt to duplicate pitcher entry: %s %s %s" % (current_pitcher.name,
                                                                pregame_pitcher_entry.team,
                                                                pregame_pitcher_entry.opposing_team)
        database_session.rollback()
    except PitcherNotFound as e:
        print e

    database_session.close()


class HitterNotFound(Exception):
    def __init__(self, id_str):
        super(HitterNotFound, self).__init__("Hitter '%s' not found in the database" % id_str)


class PitcherNotFound(Exception):
    def __init__(self, id_str):
        super(PitcherNotFound, self).__init__("Pitcher '%s' not found in the database" % id_str)


def get_hitter_stats(batter_id, pitcher_id, team, pitcher_hand, database_session):
    """ Get pregame stats for the given hitter
    :param batter_id: unique Rotowire ID for the corresponding hitter
    :param pitcher_id: unique Rotowire ID for the corresponing pitcher
    :param team: team abbreviation for the corresponding hitter
    :param pitcher_hand: a str representation of the hand the pitcher throws with ("L" or "R")
    :param database_session: SQLAlchemy database session
    :return: a PregameHitterGameEntry object without the predicted_draftkings_points field populated
    """
    pregame_hitter_entry = PregameHitterGameEntry()
    pregame_hitter_entry.rotowire_id = batter_id
    pregame_hitter_entry.pitcher_id = pitcher_id
    pregame_hitter_entry.team = team

    # Career stats
    hitter_entry = database_session.query(HitterEntry).get(batter_id)
    if hitter_entry is None:
        raise HitterNotFound(batter_id)

    hitter_career_soup = get_hitter_page_career_soup(hitter_entry.baseball_reference_id)
    try:
        career_stats = get_career_hitting_stats(hitter_entry.baseball_reference_id, hitter_career_soup)
        pregame_hitter_entry.career_pa = int(career_stats["PA"])
        pregame_hitter_entry.career_ab = int(career_stats["AB"])
        pregame_hitter_entry.career_r = int(career_stats["R"])
        pregame_hitter_entry.career_h = int(career_stats["H"])
        pregame_hitter_entry.career_hr = int(career_stats["HR"])
        pregame_hitter_entry.career_rbi = int(career_stats["RBI"])
        pregame_hitter_entry.career_sb = int(career_stats["SB"])
        pregame_hitter_entry.career_cs = int(career_stats["CS"])
        pregame_hitter_entry.career_bb = int(career_stats["BB"])
        pregame_hitter_entry.career_so = int(career_stats["SO"])
    #TODO: add ColumnNotFound exception to BaseballReference
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

    try:
        vs_hand_stats = get_vs_hand_hitting_stats(hitter_entry.baseball_reference_id, pitcher_hand, hitter_career_soup)
        pregame_hitter_entry.vs_hand_pa = int(vs_hand_stats["PA"])
        pregame_hitter_entry.vs_hand_ab = int(vs_hand_stats["AB"])
        pregame_hitter_entry.vs_hand_r = int(vs_hand_stats["R"])
        pregame_hitter_entry.vs_hand_h = int(vs_hand_stats["H"])
        pregame_hitter_entry.vs_hand_hr = int(vs_hand_stats["HR"])
        pregame_hitter_entry.vs_hand_rbi = int(vs_hand_stats["RBI"])
        pregame_hitter_entry.vs_hand_sb = int(vs_hand_stats["SB"])
        pregame_hitter_entry.vs_hand_cs = int(vs_hand_stats["CS"])
        pregame_hitter_entry.vs_hand_bb = int(vs_hand_stats["BB"])
        pregame_hitter_entry.vs_hand_so = int(vs_hand_stats["SO"])
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

    # Recent stats
    try:
        recent_stats = get_recent_hitting_stats(hitter_entry.baseball_reference_id, hitter_career_soup)
        pregame_hitter_entry.recent_pa = int(recent_stats["PA"])
        pregame_hitter_entry.recent_ab = int(recent_stats["AB"])
        pregame_hitter_entry.recent_r = int(recent_stats["R"])
        pregame_hitter_entry.recent_h = int(recent_stats["H"])
        pregame_hitter_entry.recent_hr = int(recent_stats["HR"])
        pregame_hitter_entry.recent_rbi = int(recent_stats["RBI"])
        pregame_hitter_entry.recent_sb = int(recent_stats["SB"])
        pregame_hitter_entry.recent_cs = int(recent_stats["CS"])
        pregame_hitter_entry.recent_bb = int(recent_stats["BB"])
        pregame_hitter_entry.recent_so = int(recent_stats["SO"])
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

    # Season stats
    try:
        season_stats = get_season_hitting_stats(hitter_entry.baseball_reference_id)
        pregame_hitter_entry.season_pa = int(season_stats["PA"])
        pregame_hitter_entry.season_ab = int(season_stats["AB"])
        pregame_hitter_entry.season_r = int(season_stats["R"])
        pregame_hitter_entry.season_h = int(season_stats["H"])
        pregame_hitter_entry.season_hr = int(season_stats["HR"])
        pregame_hitter_entry.season_rbi = int(season_stats["RBI"])
        pregame_hitter_entry.season_sb = int(season_stats["SB"])
        pregame_hitter_entry.season_cs = int(season_stats["CS"])
        pregame_hitter_entry.season_bb = int(season_stats["BB"])
        pregame_hitter_entry.season_so = int(season_stats["SO"])
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

    # Career versus this pitcher
    pitcher_entry = database_session.query(PitcherEntry).get(pregame_hitter_entry.pitcher_id)
    # Couldn't find the pitcher, just continue and use default values
    if pitcher_entry is None:
        return pregame_hitter_entry
    else:
        try:
            vs_pitcher_stats = get_vs_pitcher_stats(hitter_entry.baseball_reference_id,
                                                                      pitcher_entry.baseball_reference_id)
            pregame_hitter_entry.vs_pa = int(vs_pitcher_stats["PA"])
            pregame_hitter_entry.vs_ab = int(vs_pitcher_stats["AB"])
            pregame_hitter_entry.vs_h = int(vs_pitcher_stats["H"])
            pregame_hitter_entry.vs_hr = int(vs_pitcher_stats["HR"])
            pregame_hitter_entry.vs_rbi = int(vs_pitcher_stats["RBI"])
            pregame_hitter_entry.vs_bb = int(vs_pitcher_stats["BB"])
            pregame_hitter_entry.vs_so = int(vs_pitcher_stats["SO"])
        except (TableNotFound, TableRowNotFound, DidNotFacePitcher) as e:
            print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

        return pregame_hitter_entry


def get_pitcher_stats(pitcher_id, team, opposing_team, database_session, game_date=None):
    """ Get pregame stats for the given pitcher
    :param pitcher_id: unique Rotowire ID for the corresponing pitcher
    :param team: team abbreviation for the corresponding pitcher
    :param opposing_team: team abbreviation for the team the pitcher is facing
    :param database_session: SQLAlchemy database session
    :param game_date: the date of the game (in the following form yyyy-mm-dd)
    :return: a PregamePitcherGameEntry object without the predicted_draftkings_points field populated
    """
    pregame_pitcher_entry = PregamePitcherGameEntry()
    pregame_pitcher_entry.rotowire_id = pitcher_id
    pregame_pitcher_entry.team = team
    pregame_pitcher_entry.opposing_team = opposing_team
    if game_date is None:
        game_date = date.today()
    pregame_pitcher_entry.game_date = game_date

    # Career stats
    pitcher_entry = database_session.query(PitcherEntry).get(pitcher_id)
    if pitcher_entry is None:
        raise PitcherNotFound(pitcher_id)

    pitcher_career_soup = get_pitcher_page_career_soup(pitcher_entry.baseball_reference_id)
    try:
        career_stats = get_career_pitching_stats(pitcher_entry.baseball_reference_id, pitcher_career_soup)
        pregame_pitcher_entry.career_bf = int(career_stats["BF"])
        pregame_pitcher_entry.career_ip = float(career_stats["IP"])
        pregame_pitcher_entry.career_h = int(career_stats["H"])
        pregame_pitcher_entry.career_hr = int(career_stats["HR"])
        pregame_pitcher_entry.career_er = int(career_stats["ER"])
        pregame_pitcher_entry.career_bb = int(career_stats["BB"])
        pregame_pitcher_entry.career_so = int(career_stats["SO"])
        pregame_pitcher_entry.career_wins = int(career_stats["W"])
        pregame_pitcher_entry.career_losses = int(career_stats["L"])
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(pitcher_entry.first_name), str(pitcher_entry.last_name)

    opposing_lineup = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == game_date,
                                                                            PregameHitterGameEntry.opposing_team == opposing_team)
    for hitter in opposing_lineup:
        pregame_pitcher_entry.vs_h += hitter.vs_h
        pregame_pitcher_entry.vs_bb += hitter.vs_bb
        pregame_pitcher_entry.vs_so += hitter.vs_so
        pregame_pitcher_entry.vs_hr += hitter.vs_hr
        pregame_pitcher_entry.vs_bf += hitter.vs_pa
        # Approximate earned runs by the RBIs of opposing hitters
        pregame_pitcher_entry.vs_er += hitter.vs_rbi

    # Recent stats
    try:
        recent_stats = get_recent_pitcher_stats(pitcher_entry.baseball_reference_id, pitcher_career_soup)
        pregame_pitcher_entry.recent_bf = int(recent_stats["BF"])
        pregame_pitcher_entry.recent_ip = float(recent_stats["IP"])
        pregame_pitcher_entry.recent_h = int(recent_stats["H"])
        pregame_pitcher_entry.recent_hr = int(recent_stats["HR"])
        pregame_pitcher_entry.recent_er = int(recent_stats["ER"])
        pregame_pitcher_entry.recent_bb = int(recent_stats["BB"])
        pregame_pitcher_entry.recent_so = int(recent_stats["SO"])
        pregame_pitcher_entry.recent_wins = int(recent_stats["W"])
        pregame_pitcher_entry.recent_losses = int(recent_stats["L"])
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(pitcher_entry.first_name), str(pitcher_entry.last_name)

    #Season stats
    try:
        season_stats = get_season_pitcher_stats(pitcher_entry.baseball_reference_id)
        pregame_pitcher_entry.season_bf = int(season_stats["BF"])
        pregame_pitcher_entry.season_ip = float(season_stats["IP"])
        pregame_pitcher_entry.season_h = int(season_stats["H"])
        pregame_pitcher_entry.season_hr = int(season_stats["HR"])
        pregame_pitcher_entry.season_er = int(season_stats["ER"])
        pregame_pitcher_entry.season_bb = int(season_stats["BB"])
        pregame_pitcher_entry.season_so = int(season_stats["SO"])
        pregame_pitcher_entry.season_wins = int(season_stats["W"])
        pregame_pitcher_entry.season_losses = int(season_stats["L"])
    except (TableNotFound, TableRowNotFound) as e:
        print str(e), "with", str(pitcher_entry.first_name), str(pitcher_entry.last_name)

    return pregame_pitcher_entry


def table_entry_to_int(entry):
    return int(entry.replace(",", ""))


def mine_yesterdays_results(database_session):
    """ Mine the results of yesterday's game for all hitters and pitchers in the database
    :param database_session: SQLAlchemy database object
    """
    # Query the database for all hitter game entries from yesterday
    hitter_entries = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == (date.today() - timedelta(days=1)))
    for pregame_hitter_entry in hitter_entries:
        hitter_entry = database_session.query(HitterEntry).get(pregame_hitter_entry.rotowire_id)
        try:
            stat_row_dict = get_yesterdays_hitting_game_log(hitter_entry.baseball_reference_id)
        except TableRowNotFound:
            print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % (hitter_entry.first_name,
                                                                                         hitter_entry.last_name,
                                                                                         pregame_hitter_entry.game_date,
                                                                                         pregame_hitter_entry.opposing_team)
            database_session.delete(pregame_hitter_entry)
            database_session.commit()
            continue

        postgame_hitter_entry = PostgameHitterGameEntry()
        postgame_hitter_entry.rotowire_id = hitter_entry.rotowire_id
        postgame_hitter_entry.game_date = pregame_hitter_entry.game_date
        postgame_hitter_entry.game_h = int(stat_row_dict["H"])
        postgame_hitter_entry.game_bb = int(stat_row_dict["BB"])
        postgame_hitter_entry.game_hbp = int(stat_row_dict["HBP"])
        postgame_hitter_entry.game_r = int(stat_row_dict["R"])
        postgame_hitter_entry.game_sb = int(stat_row_dict["SB"])
        postgame_hitter_entry.game_hr = int(stat_row_dict["HR"])
        postgame_hitter_entry.game_rbi = int(stat_row_dict["RBI"])
        postgame_hitter_entry.game_2b = int(stat_row_dict["2B"])
        postgame_hitter_entry.game_3b = int(stat_row_dict["3B"])
        postgame_hitter_entry.game_1b = postgame_hitter_entry.game_h - postgame_hitter_entry.game_2b - \
                                        postgame_hitter_entry.game_3b - postgame_hitter_entry.game_hr
        postgame_hitter_entry.actual_draftkings_points = get_hitter_points(postgame_hitter_entry)
        try:
            database_session.add(postgame_hitter_entry)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            print "Attempt to duplicate hitter postgame results: %s %s %s %s" % (hitter_entry.first_name,
                                                                                 hitter_entry.last_name,
                                                                                 hitter_entry.team,
                                                                                 pregame_hitter_entry.game_date)

    # Query the database for all hitter game entries from yesterday
    pitcher_entries = database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == (date.today() - timedelta(days=1)))
    for pregame_pitcher_entry in pitcher_entries:
        pitcher_entry = database_session.query(PitcherEntry).get(pregame_pitcher_entry.rotowire_id)
        print "Mining yesterday for %s %s" % (pitcher_entry.first_name, pitcher_entry.last_name)
        try:
            stat_row_dict = get_pitching_game_log(pitcher_entry.baseball_reference_id)
        except TableRowNotFound:
            print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % \
                  (pitcher_entry.first_name,
                   pitcher_entry.last_name,
                   pregame_pitcher_entry.game_date,
                   pregame_pitcher_entry.opposing_team)

            database_session.delete(pregame_pitcher_entry)
            database_session.commit()
            continue

        postgame_pitcher_entry = PostgamePitcherGameEntry()
        postgame_pitcher_entry.rotowire_id = pitcher_entry.rotowire_id
        postgame_pitcher_entry.game_date = pregame_pitcher_entry.game_date
        postgame_pitcher_entry.game_ip = float(stat_row_dict["IP"])
        postgame_pitcher_entry.game_so = int(stat_row_dict["SO"])
        if str(stat_row_dict["Dec"])[0] == "W":
            postgame_pitcher_entry.game_wins = 1
        postgame_pitcher_entry.game_er = int(stat_row_dict["ER"])
        postgame_pitcher_entry.game_er = int(stat_row_dict["ER"])
        postgame_pitcher_entry.game_h = int(stat_row_dict["H"])
        postgame_pitcher_entry.game_bb = int(stat_row_dict["BB"])
        postgame_pitcher_entry.game_hbp = int(stat_row_dict["HBP"])
        if stat_row_dict["Inngs"] == "CG":
            postgame_pitcher_entry.game_cg = 1
        if stat_row_dict["Inngs"] == "SHO":
            postgame_pitcher_entry.game_cgso = 1
        if postgame_pitcher_entry.game_cg == 1 and postgame_pitcher_entry.game_h == 0:
            postgame_pitcher_entry.game_no_hitter = 1
        postgame_pitcher_entry.actual_draftkings_points = get_pitcher_points(postgame_pitcher_entry)
        try:
            database_session.add(postgame_pitcher_entry)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            print "Attempt to duplicate pitcher postgame results: %s %s %s %s" % (pitcher_entry.first_name,
                                                                                  pitcher_entry.last_name,
                                                                                  pregame_pitcher_entry.opposing_team,
                                                                                  postgame_pitcher_entry.game_date)


def get_table_row_dict(soup, table_name, table_row_label, table_column_label):
    """ Get a dictionary representation of the given row in the table
    :param soup: BeautifulSoup object containing a single "table" HTML object
    :param table_name: HTML "id" field for the table
    :param table_row_label: HTML label for the row of the table
    :param table_column_label: HTML label for the column
    :return: dictionary representation of the given row
    """
    results_table = soup.find("table", {"id": table_name})
    if results_table is None:
        raise TableNotFound(table_name)

    table_header_list = results_table.find("thead").findAll("th")
    table_header_list = [x.text for x in table_header_list]
    stat_rows = results_table.find("tbody").findAll("tr")

    for stat_row in stat_rows:
        #Create a dictionary of the stat attributes
        stat_dict = dict()
        stat_entries = stat_row.findAll("td")
        for i in range(0, len(table_header_list)):
            if stat_entries[i].text == "":
                stat_dict[table_header_list[i]] = 0
            else:
                stat_dict[table_header_list[i]] = stat_entries[i].text
        try:
            if stat_dict[table_column_label] == table_row_label:
                return stat_dict
        # We have reached the end of the year-by-year stats, just end
        except ValueError:
            break

    # TODO: add a TableRowNotFound exception
    raise TableNotFound(table_name)


def get_wind_speed(soup):
    """ Extract the wind speed from the Rotowire game soup
    :param soup: Rotowire soup for the individual game
    :return: an integer representation of the wind speed (negative for "In", positive for "Out", zero otherwise)
    """
    wind_text = soup.find("div", {"class": WIND_LABEL}).text
    wind_words = wind_text.strip().split()
    if wind_words[len(wind_words)-1] == "Out":
        return int(wind_words[1])
    elif wind_words[len(wind_words)-1] == "In":
        return -1*int(wind_words[1])

    return 0


class UmpDataNotFound(Exception):

    def __init__(self):
        super(UmpDataNotFound, self).__init__("The ump data was not found in the soup")


def get_ump_ks_per_game(soup):
    """ Extract the strikeouts per 9 innings for the ump for a given game
    :param soup: Rotowire soup for the individual game
    :return: float representation of the strikeouts per game
    """
    span15s = soup.findAll("div", {"class": "span15"})
    for span15 in span15s:
        node = span15.find("b")
        if node is not None:
            if node.text.strip() == "Ump:":
                ump_text = span15.text
                ump_words = ump_text.strip().split()
                for i in range(0, len(ump_words)):
                    if ump_words[i] == "K/9:":
                        return float(ump_words[i+1])

    raise UmpDataNotFound


def get_ump_runs_per_game(soup):
    """ Extract the strikeouts per 9 innings for the ump for a given game
    :param soup: Rotowire soup for the individual game
    :return: float representation of the strikeouts per game
    """
    span15s = soup.findAll("div", {"class": "span15"})
    for span15 in span15s:
        node = span15.find("b")
        if node is not None:
            if node.text.strip() == "Ump:":
                ump_text = span15.text
                ump_words = ump_text.strip().split()
                for i in range(0, len(ump_words)):
                    if ump_words[i] == "R/9:":
                        return float(ump_words[i+1].replace("&nbsp", ""))

    raise UmpDataNotFound

# Two-way dictionary
team_dict = bidict.bidict(ARI="Arizona Diamondbacks",
                          ATL="Atlanta Braves",
                          BAL="Baltimore Orioles",
                          BOS="Boston Red Sox",
                          CHC="Chicago Cubs",
                          CWS="Chicago White Sox",
                          CIN="Cincinnati Reds",
                          CLE="Cleveland Indians",
                          COL="Colorado Rockies",
                          DET="Detroit Tigers",
                          HOU="Houston Astros",
                          KC="Kansas City Royals",
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
                          SD="San Diego Padres",
                          SEA="Seattle Mariners",
                          SF="San Francisco Giants",
                          STL="St. Louis Cardinals",
                          TB="Tampa Bay Rays",
                          TEX="Texas Rangers",
                          TOR="Toronto Blue Jays",
                          WAS="Washington Nationals")
