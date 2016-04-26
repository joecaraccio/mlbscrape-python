from datetime import date

from baseball_reference import BaseballReference
from beautiful_soup_helper import BeautifulSoupHelper

from sql.hitter_entry import HitterEntry
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.pitcher_entry import PitcherEntry
from sqlalchemy.exc import IntegrityError
import bidict


class RotoWire(object):
    """ Class for implementing all RotoWire functionality
    """

    # Daily lineups relevant HTML labels
    DAILY_LINEUPS_URL = "http://www.rotowire.com/baseball/daily_lineups.htm"
    GAME_REGION_LABEL = "offset1 span15"
    TEAM_REGION_LABEL = "span15 dlineups-topbox"
    AWAY_TEAM_REGION_LABEL = "span5 dlineups-topboxleft"
    HOME_TEAM_REGION_LABEL = "span5 dlineups-topboxright"
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

    class PlayerStruct(object):
        def __init__(self, name, team, rotowire_id, position, hand):
            self.name = name
            self.team = team
            self.rotowire_id = rotowire_id
            self.position = position
            self.hand = hand

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

    class HomeAwayEnum:
        AWAY = 0
        HOME = 1

    @staticmethod
    def mine_pregame_stats(database_session):
        """ Mine the hitter/pitcher stats and predict the outcomes and commit to the database session
        :param database-_session: SQLAlchemy database session
        """
        games = RotoWire.get_game_lineups()
        RotoWire.update_ids(games, database_session)
        RotoWire.get_pregame_hitting_stats(games, database_session)
        RotoWire.get_pregame_pitching_stats(games, database_session)

    @staticmethod
    def get_game_lineups():
        """ Mine the RotoWire daily lineups page and get the players' name, team, and RotoWire ID
        Note: longer names are abbreviated by RotoWire and need to be resolved by another source
        :return: list of Game objects representing the lineups for the day
        """
        #TODO: add feature to look if the lineup is pending
        #TODO: add feature to look if it's going to rain
        lineup_soup = BeautifulSoupHelper.get_soup_from_url(RotoWire.DAILY_LINEUPS_URL)
        header_nodes = lineup_soup.findAll("div", {"class": RotoWire.TEAM_REGION_LABEL})
        games = list()
        for header_node in header_nodes:
            game_node = header_node.parent
            home_team_lineup = list()
            away_team_lineup = list()
            away_team_abbreviation = game_node.find("div", {"class": RotoWire.AWAY_TEAM_REGION_LABEL}).text.split()[0]
            home_team_abbreviation = game_node.find("div", {"class": RotoWire.HOME_TEAM_REGION_LABEL}).text.split()[0]
            game_main_soup = game_node.find("div", {"class": RotoWire.LINEUPS_CLASS_LABEL})

            for away_player in game_main_soup.findAll("div", {"class": RotoWire.AWAY_TEAM_PLAYER_LABEL}):
                away_team_lineup.append(RotoWire.get_hitter(away_player, away_team_abbreviation))
            for home_player in game_main_soup.findAll("div", {"class": RotoWire.HOME_TEAM_PLAYER_LABEL}):
                home_team_lineup.append(RotoWire.get_hitter(home_player, home_team_abbreviation))

            pitchers = game_node.find("div", RotoWire.PITCHERS_REGION_LABEL).findAll("div")
            away_team_pitcher = RotoWire.get_pitcher(pitchers[0], away_team_abbreviation)
            home_team_pitcher = RotoWire.get_pitcher(pitchers[1], home_team_abbreviation)

            current_game = RotoWire.Game(away_team_lineup, away_team_pitcher, home_team_lineup, home_team_pitcher)
            if current_game.is_valid():
                games.append(current_game)
            else:
                print "Game between %s and %s is not valid." % (away_team_abbreviation, home_team_abbreviation)


        return games

    @staticmethod
    def get_id(soup):
        """ Get the RotoWire ID from a BeautifulSoup node
        :param soup: BeautifulSoup object of the player in the daily lineups page
        """
        return soup.find("a").get("href").split("id=")[1]

    @staticmethod
    def get_hitter(soup, team):
        """ Get the hitter info from a BeautifulSoup node
        """
        rotowire_id = RotoWire.get_id(soup)
        name = RotoWire.get_name_from_id(rotowire_id)
        hand = RotoWire.get_hand(soup)
        position = soup.find("div", {"class": RotoWire.POSITION_CLASS_LABEL}).text
        return RotoWire.PlayerStruct(name, team, rotowire_id, position, hand)

    @staticmethod
    def get_pitcher(soup, team):
        """ Get the hitter info from a BeautifulSoup node
        """
        rotowire_id = RotoWire.get_id(soup)
        hand = RotoWire.get_hand(soup)
        name = RotoWire.get_name_from_id(rotowire_id)
        return RotoWire.PlayerStruct(name, team, rotowire_id, "P", hand)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_hand(soup):
        """
        :param soup: BeautifulSoup node of the player
        :return: Hand of the player
        """
        return soup.find("span", {"class": RotoWire.HAND_CLASS_LABEL}).text.strip().replace("(", "").replace(")", "")

    @staticmethod
    def update_lineup_ids(lineup, database_session):
        hitter_soup = BaseballReference.get_hitter_soup()
        for current_player in lineup:
            name = current_player.name.split()
            first_name = name[0]
            last_name = " ".join(str(x) for x in name[1:len(name)])
            db_query = database_session.query(HitterEntry).filter(HitterEntry.rotowire_id == current_player.rotowire_id)
            # Found unique entry, check to make sure the team matches the database
            if db_query.count() == 1:
                if db_query[0].team == current_player.team:
                    continue
                # Update the player's team in the database
                else:
                    db_query[0].team = current_player.team
                    database_session.commit()
            # Found no entries, create a bare bones entry with just the name and id
            else:
                try:
                    baseball_reference_id = BaseballReference.get_hitter_id(first_name + " " + last_name,
                                                                            BaseballReference.team_dict.inv[RotoWire.team_dict[current_player.team]],
                                                                            date.today().year,
                                                                            hitter_soup)
                except BaseballReference.NameNotFound:
                    print "Skipping committing this hitter '%s %s'." % (first_name, last_name)
                    continue

                RotoWire.create_new_hitter_entry(current_player, baseball_reference_id, database_session)

    @staticmethod
    def update_pitcher_id(pitcher, database_session):
        pitcher_soup = BaseballReference.get_pitcher_soup()
        name = pitcher.name.split()
        first_name = name[0]
        last_name = " ".join(str(x) for x in name[1:len(name)])
        db_query = database_session.query(PitcherEntry).filter(PitcherEntry.rotowire_id == pitcher.rotowire_id)
        # Found unique entry, check to make sure the team matches the database
        if db_query.count() == 1:
            if db_query[0].team == pitcher.team:
                return
            # Update the player's team in the database
            else:
                db_query[0].team = pitcher.team
                database_session.commit()
        # Found no entries, create a bare bones entry with just the name and id
        else:
            try:
                baseball_reference_id = BaseballReference.get_pitcher_id(first_name + " " + last_name,
                                                                        BaseballReference.team_dict.inv[RotoWire.team_dict[pitcher.team]],
                                                                        date.today().year,
                                                                        pitcher_soup)
            except BaseballReference.NameNotFound:
                print "Skipping committing this pitcher '%s %s'." % (first_name, last_name)
                return

            RotoWire.create_new_pitcher_entry(pitcher, baseball_reference_id, database_session)

    @staticmethod
    def update_ids(games, database_session):
        """Cycle through the lineups and make sure every ID is located in the HitterEntry table of the MlbDatabasecreate_new_hitter
        :param game_lineups: list of Game objects
        :param database_session: SQLAlchemy database session
        """
        for game in games:
            RotoWire.update_lineup_ids(game.away_lineup, database_session)
            RotoWire.update_pitcher_id(game.away_pitcher, database_session)
            RotoWire.update_lineup_ids(game.home_lineup, database_session)
            RotoWire.update_pitcher_id(game.home_pitcher, database_session)

    @staticmethod
    def get_name_from_id(rotowire_id):
        """ Use the acquired RotoWire ID to resolve the name in case it is too long for the
        daily lineups page.
        :param rotowire_id: unique ID for a player in RotoWire
        :return: str representation of the name of the player
        """
        player_soup = BeautifulSoupHelper.get_soup_from_url(RotoWire.PLAYER_PAGE_BASE_URL + str(rotowire_id))
        return player_soup.find("div", {"class": RotoWire.PLAYER_PAGE_LABEL}).find("h1").text.strip()

    @staticmethod
    def get_pregame_hitting_stats(games, database_session):
        for game in games:
            for current_hitter in game.away_lineup:
                pitcher_hand = game.home_pitcher.hand
                print "Mining %s." % current_hitter.name
                try:
                    pregame_hitter_entry = RotoWire.get_hitter_stats(current_hitter.rotowire_id,
                                                                 game.home_pitcher.rotowire_id,
                                                                 current_hitter.team,
                                                                 pitcher_hand,
                                                                 database_session)
                    pregame_hitter_entry.game_id = RotoWire.get_game_id(game.away_lineup[0].team, game.home_lineup[0].team)
                    RotoWire.predict_draftkings_points(pregame_hitter_entry)
                    database_session.add(pregame_hitter_entry)
                    database_session.commit()
                except RotoWire.HitterNotFound as e:
                    print e
                except IntegrityError:
                    print "Attempt to duplicate hitter entry: %s %s" % (current_hitter.name,
                                                                        pregame_hitter_entry.game_id)
                    database_session.rollback()
            for current_hitter in game.home_lineup:
                pitcher_hand = game.away_pitcher.hand
                print "Mining %s." % current_hitter.name
                try:
                    pregame_hitter_entry = RotoWire.get_hitter_stats(current_hitter.rotowire_id,
                                                                 game.away_pitcher.rotowire_id,
                                                                 current_hitter.team,
                                                                 pitcher_hand,
                                                                 database_session)
                    pregame_hitter_entry.game_id = RotoWire.get_game_id(game.away_lineup[0].team, game.home_lineup[0].team)
                    RotoWire.predict_draftkings_points(pregame_hitter_entry)
                    database_session.add(pregame_hitter_entry)
                    database_session.commit()
                except RotoWire.HitterNotFound as e:
                    print e
                except IntegrityError:
                    print "Attempt to duplicate hitter entry: %s %s" % (current_hitter.name,
                                                                        pregame_hitter_entry.game_id)
                    database_session.rollback()

    @staticmethod
    def predict_draftkings_points(pregame_hitter_entry):
        return

    @staticmethod
    def get_pregame_pitching_stats(games, database_session):
        for game in games:
            current_pitcher = game.away_pitcher
            print "Mining %s." % current_pitcher.name
            game_id = RotoWire.get_game_id(game.away_pitcher.team, game.home_pitcher.team)
            try:
                pregame_pitcher_entry = RotoWire.get_pitcher_stats(current_pitcher.rotowire_id,
                                                                   current_pitcher.team,
                                                                   game_id,
                                                                   database_session)

                RotoWire.predict_draftkings_points(pregame_pitcher_entry)
                database_session.add(pregame_pitcher_entry)
                database_session.commit()
            except IntegrityError:
                print "Attempt to duplicate pitcher entry: %s %s" % (pregame_pitcher_entry.name,
                                                                     pregame_pitcher_entry.game_id)
                database_session.rollback()
            except RotoWire.PitcherNotFound as e:
                print e

            current_pitcher = game.home_pitcher
            print "Mining %s." % current_pitcher.name
            game_id = RotoWire.get_game_id(game.away_pitcher.team, game.home_pitcher.team)
            try:
                pregame_pitcher_entry = RotoWire.get_pitcher_stats(current_pitcher.rotowire_id,
                                                                   current_pitcher.team,
                                                                   game_id,
                                                                   database_session)

                RotoWire.predict_draftkings_points(pregame_pitcher_entry)
                database_session.add(pregame_pitcher_entry)
                database_session.commit()
            except IntegrityError:
                print "Attempt to duplicate pitcher entry: %s %s" % (pregame_pitcher_entry.name,
                                                                     pregame_pitcher_entry.game_id)
                database_session.rollback()
            except RotoWire.PitcherNotFound as e:
                print e

    class HitterNotFound(Exception):
        def __init__(self, id_str):
            super(RotoWire.HitterNotFound, self).__init__("Hitter '%s' not found in the database" %
                                                                 id_str)

    class PitcherNotFound(Exception):
        def __init__(self, id_str):
            super(RotoWire.PitcherNotFound, self).__init__("Pitcher '%s' not found in the database" %
                                                                 id_str)

    @staticmethod
    def get_hitter_stats(batter_id, pitcher_id, team, pitcher_hand, database_session):
        """ Get the career, last 14 day, vs hand stats from the RotoWire player page, get t
        :param rotowire_id: the RotoWire unique ID of this player
        :param pitcher_hand: a str representation of the hand the pitcher throws with ("L" or "R")
        :return: a PregameHitterGameEntry object without the predicted_draftkings_points field populated
        """
        pregame_hitter_entry = PregameHitterGameEntry()
        pregame_hitter_entry.rotowire_id = batter_id
        pregame_hitter_entry.pitcher_id = pitcher_id
        pregame_hitter_entry.team = team

        # Career stats
        hitter_entries = database_session.query(HitterEntry).filter(HitterEntry.rotowire_id == batter_id)
        if hitter_entries.count() == 0:
            raise RotoWire.HitterNotFound(batter_id)
        hitter_entry = hitter_entries[0]
        hitter_career_soup = BaseballReference.get_hitter_page_career_soup(hitter_entry.baseball_reference_id)
        career_stats = BaseballReference.get_career_hitting_stats(hitter_entry.baseball_reference_id, hitter_career_soup)
        pregame_hitter_entry.career_ab = career_stats.ab
        pregame_hitter_entry.career_r = career_stats.r
        pregame_hitter_entry.career_h = career_stats.h
        pregame_hitter_entry.career_hr = career_stats.hr
        pregame_hitter_entry.career_rbi = career_stats.rbi
        pregame_hitter_entry.career_sb = career_stats.sb
        pregame_hitter_entry.career_cs = career_stats.cs
        pregame_hitter_entry.career_bb = career_stats.bb
        pregame_hitter_entry.career_so = career_stats.so

        # Vs hand of the opposing pitcher
        if pitcher_hand == "L":
            pitcher_hand_lr = BaseballReference.HandEnum.LHP
        elif pitcher_hand == "R":
            pitcher_hand_lr = BaseballReference.HandEnum.RHP
        else:
            print "Invalid pitcher hand %i" % pitcher_hand
            assert 0
        vs_hand_stats = BaseballReference.get_vs_hand_hitting_stats(hitter_entry.baseball_reference_id, pitcher_hand_lr, hitter_career_soup)
        pregame_hitter_entry.vs_hand_ab = vs_hand_stats.ab
        pregame_hitter_entry.vs_hand_r = vs_hand_stats.r
        pregame_hitter_entry.vs_hand_h = vs_hand_stats.h
        pregame_hitter_entry.vs_hand_hr = vs_hand_stats.hr
        pregame_hitter_entry.vs_hand_rbi = vs_hand_stats.rbi
        pregame_hitter_entry.vs_hand_sb = vs_hand_stats.sb
        pregame_hitter_entry.vs_hand_cs = vs_hand_stats.cs
        pregame_hitter_entry.vs_hand_bb = vs_hand_stats.bb
        pregame_hitter_entry.vs_hand_so = vs_hand_stats.so

        # Recent stats
        recent_stats = BaseballReference.get_recent_hitting_stats(hitter_entry.baseball_reference_id, hitter_career_soup)
        pregame_hitter_entry.recent_ab = recent_stats.ab
        pregame_hitter_entry.recent_r = recent_stats.r
        pregame_hitter_entry.recent_h = recent_stats.h
        pregame_hitter_entry.recent_hr = recent_stats.hr
        pregame_hitter_entry.recent_rbi = recent_stats.rbi
        pregame_hitter_entry.recent_sb = recent_stats.sb
        pregame_hitter_entry.recent_cs = recent_stats.cs
        pregame_hitter_entry.recent_bb = recent_stats.bb
        pregame_hitter_entry.recent_so = recent_stats.so

        #Season stats
        season_stats = BaseballReference.get_season_hitting_stats(hitter_entry.baseball_reference_id)
        pregame_hitter_entry.season_ab = season_stats.ab
        pregame_hitter_entry.season_r = season_stats.r
        pregame_hitter_entry.season_h = season_stats.h
        pregame_hitter_entry.season_hr = season_stats.hr
        pregame_hitter_entry.season_rbi = season_stats.rbi
        pregame_hitter_entry.season_sb = season_stats.sb
        pregame_hitter_entry.season_cs = season_stats.cs
        pregame_hitter_entry.season_bb = season_stats.bb
        pregame_hitter_entry.season_so = season_stats.so

        # Career versus this pitcher
        pitcher_entries = database_session.query(PitcherEntry).filter(PitcherEntry.rotowire_id == pregame_hitter_entry.pitcher_id)
        # Couldn't find the pitcher, just continue and use default values
        if pitcher_entries.count() == 0:
            return pregame_hitter_entry
        else:
            pitcher_entry = pitcher_entries[0]
            vs_pitcher_stats = BaseballReference.get_vs_pitcher_stats(pitcher_entry.baseball_reference_id,
                                                                  pitcher_id)
            pregame_hitter_entry.vs_ab = vs_pitcher_stats.ab
            pregame_hitter_entry.vs_h = vs_pitcher_stats.h
            pregame_hitter_entry.vs_hr = vs_pitcher_stats.hr
            pregame_hitter_entry.vs_rbi = vs_pitcher_stats.rbi
            pregame_hitter_entry.vs_bb = vs_pitcher_stats.bb
            pregame_hitter_entry.vs_so = vs_pitcher_stats.so

            return pregame_hitter_entry

    @staticmethod
    def get_pitcher_stats(pitcher_id, team, game_id, database_session):
        """ Get the career, last 14 day, vs hand stats from the RotoWire player page, get t
        :param rotowire_id: the RotoWire unique ID of this player
        :param pitcher_hand: a str representation of the hand the pitcher throws with ("L" or "R")
        :return: a PregameHitterGameEntry object without the predicted_draftkings_points field populated
        """
        pregame_hitter_entry = PregamePitcherGameEntry()
        pregame_hitter_entry.rotowire_id = pitcher_id
        pregame_hitter_entry.team = team
        pregame_hitter_entry.game_id = game_id

        # Career stats
        pitcher_entries = database_session.query(PitcherEntry).filter(PitcherEntry.rotowire_id == pitcher_id)
        if pitcher_entries.count() == 0:
            raise RotoWire.PitcherNotFound(pitcher_id)
        pitcher_entry = pitcher_entries[0]

        pitcher_career_soup = BaseballReference.get_pitcher_page_career_soup(pitcher_entry.baseball_reference_id)

        career_stats = BaseballReference.get_career_pitching_stats(pitcher_entry.baseball_reference_id, pitcher_career_soup)
        pregame_hitter_entry.career_bf = career_stats.batters_faced
        pregame_hitter_entry.career_ip = career_stats.ip
        pregame_hitter_entry.career_h = career_stats.h
        pregame_hitter_entry.career_hr = career_stats.hr
        pregame_hitter_entry.career_er = career_stats.er
        pregame_hitter_entry.career_bb = career_stats.bb
        pregame_hitter_entry.career_so = career_stats.so
        pregame_hitter_entry.career_wins = career_stats.wins
        pregame_hitter_entry.career_losses = career_stats.losses

        opposing_lineup = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_id == game_id,
                                                                                PregameHitterGameEntry.team != team)
        for hitter in opposing_lineup:
            pregame_hitter_entry.vs_h += hitter.vs_h
            pregame_hitter_entry.vs_bb += hitter.vs_bb
            pregame_hitter_entry.vs_so += hitter.vs_so
            pregame_hitter_entry.vs_hr += hitter.vs_hr
            # TODO: add plate apperances to hitter stats so we can accurately keep track of batters faced
            pregame_hitter_entry.vs_bf += hitter.vs_ab
            # Approximate earned runs by the RBIs of opposing hitters
            pregame_hitter_entry.vs_er += hitter.vs_rbi

        # Recent stats
        recent_stats = BaseballReference.get_recent_pitcher_stats(pitcher_entry.baseball_reference_id, pitcher_career_soup)
        pregame_hitter_entry.recent_bf = recent_stats.batters_faced
        pregame_hitter_entry.recent_ip = recent_stats.ip
        pregame_hitter_entry.recent_h = recent_stats.h
        pregame_hitter_entry.recent_hr = recent_stats.hr
        pregame_hitter_entry.recent_er = recent_stats.er
        pregame_hitter_entry.recent_bb = recent_stats.bb
        pregame_hitter_entry.recent_so = recent_stats.so
        pregame_hitter_entry.recent_wins = recent_stats.wins
        pregame_hitter_entry.recent_losses = recent_stats.losses

        #Season stats
        season_stats = BaseballReference.get_season_pitcher_stats(pitcher_entry.baseball_reference_id)
        pregame_hitter_entry.recent_bf = season_stats.batters_faced
        pregame_hitter_entry.recent_ip = season_stats.ip
        pregame_hitter_entry.recent_h = season_stats.h
        pregame_hitter_entry.recent_hr = season_stats.hr
        pregame_hitter_entry.recent_er = season_stats.er
        pregame_hitter_entry.recent_bb = season_stats.bb
        pregame_hitter_entry.recent_so = season_stats.so
        pregame_hitter_entry.recent_wins = season_stats.wins
        pregame_hitter_entry.recent_losses = season_stats.losses

        return pregame_hitter_entry

    @staticmethod
    def get_game_id(away_team, home_team, game_date=None):
        #TODO: this team naming convention doesn't match the mlb.com convention
        if game_date is None:
            game_date = date.today()

        return "gid_" + str(game_date.year) + "_" + ("%02d" % (game_date.month,)) + "_" + ("%02d" % (game_date.day,)) + \
               "_" + away_team.lower() + "mlb_" + home_team.lower() + "mlb_1"

    @staticmethod
    def table_entry_to_int(entry):
        return int(entry.replace(",", ""))

    @staticmethod
    def get_draftkings_link(daily_lineup_soup):
        return daily_lineup_soup.find("div", {"class": RotoWire.DRAFTKINGS_LINK_LABEL}).find("a").get("href")

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