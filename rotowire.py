
from beautiful_soup_helper import BeautifulSoupHelper
from hitter_entry import HitterEntry
from hitter import Hitter
from pregame_hitter import PregameHitterGameEntry
from datetime import date


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
        :param database_session: SQLAlchemy database session
        """
        games = RotoWire.get_game_lineups()
        #RotoWire.update_ids(games, database_session)
        RotoWire.get_pregame_hitting_stats(games, database_session)
        #RotoWire.get_pregame_pitching_stats(games, database_session)

    @staticmethod
    def get_game_lineups():
        """ Mine the RotoWire daily lineups page and get the players' name, team, and RotoWire ID
        Note: longer names are abbreviated by RotoWire and need to be resolved by another source
        :return: list of Game objects representing the lineups for the day
        """
        #TODO: add feature to look if the lineup is pending
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
                #TODO: this is for debugging. take it out when done
                break
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
        print "Mining %s" % name
        position = soup.find("div", {"class": RotoWire.POSITION_CLASS_LABEL}).text
        return RotoWire.PlayerStruct(name, team, rotowire_id, position, hand)

    @staticmethod
    def get_pitcher(soup, team):
        """ Get the hitter info from a BeautifulSoup node
        """
        rotowire_id = RotoWire.get_id(soup)
        hand = RotoWire.get_hand(soup)
        return RotoWire.PlayerStruct(soup.find("a").text, team, rotowire_id, "P", hand)

    @staticmethod
    def create_new_hitter_entry(player_struct, database_session):
        name = player_struct.name.split()
        first_name = name[0]
        last_name = " ".join(str(x) for x in name[1:len(name)])
        entry = HitterEntry(first_name, last_name, 0, 0, player_struct.rotowire_id, player_struct.team, 0)
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
        for current_player in lineup:
            name = current_player.name.split()
            first_name = name[0]
            last_name = " ".join(str(x) for x in name[1:len(name)])
            db_query = database_session.query(HitterEntry).filter(HitterEntry.last_name == last_name,
                                                                  HitterEntry.team == current_player.team)
            # Found unique entry, update entry with RotoWire ID
            if db_query.count() == 1:
                db_query[0].rotowire_id = current_player.rotowire_id
                database_session.commit()
            # Found multiple entries, resolve the first name next
            elif db_query.count() > 1:
                for hitter in db_query:
                    # Direct match, just update the ID and commit
                    if hitter.first_name == first_name:
                        hitter.rotowire_id = current_player.rotowire_id
                        database_session.commit()
                        # First initial matches, just update the ID and commit
                    elif hitter.first_name[0] == first_name[0]:
                        hitter.rotowire_id = current_player.rotowire_id
                        database_session.commit()
                    # First names don't really match, create a bare bones entry with just the name and id
                    else:
                        RotoWire.create_new_hitter_entry(current_player, database_session)
            # Found no entries, create a bare bones entry with just the name and id
            else:
                RotoWire.create_new_hitter_entry(current_player, database_session)

    @staticmethod
    def update_ids(games, database_session):
        """Cycle through the lineups and make sure every ID is located in the HitterEntry table of the MlbDatabase
        :param game_lineups: list of Game objects
        :param database_session: SQLAlchemy database session
        """
        for game in games:
            RotoWire.update_lineup_ids(game.away_lineup, database_session)
            RotoWire.update_lineup_ids(game.home_lineup, database_session)

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
                pregame_hitter_entry = RotoWire.get_hitter_stats(current_hitter.rotowire_id, current_hitter.team, pitcher_hand)
                pregame_hitter_entry.game_id = RotoWire.get_game_id(game.away_lineup[0].team, game.home_lineup[0].team)
                RotoWire.predict_draftkings_points(pregame_hitter_entry)
                database_session.add(pregame_hitter_entry)
                database_session.commit()
            for current_hitter in game.home_lineup:
                pitcher_hand = game.away_pitcher.hand
                pregame_hitter_entry = RotoWire.get_hitter_stats(current_hitter.rotowire_id, current_hitter.team, pitcher_hand)
                pregame_hitter_entry.game_id = RotoWire.get_game_id(game.away_lineup[0].team, game.home_lineup[0].team)
                RotoWire.predict_draftkings_points(pregame_hitter_entry)
                database_session.add(pregame_hitter_entry)
                database_session.commit()

    @staticmethod
    def predict_draftkings_points(pregame_hitter_entry):
        return

    @staticmethod
    def get_pregame_pitching_stats(games, database_session):
        #TODO: implement this function
        return
        """for game in games:

            for current_player in game.away_lineup:
                if current_player.position == "P":
                    pitching_stats.append(RotoWire.Game(RotoWire.get_pitcher_stats(current_player.rotowire_id)))
                    break
            for current_player in game.home_lineup:
                if current_player.position == "P":
                    pitching_stats.append(RotoWire.Game(RotoWire.get_pitcher_stats(current_player.rotowire_id)))
                    break
        """

    @staticmethod
    def get_hitter_stats(rotowire_id, team, pitcher_hand):
        """ Get the career, last 14 day, vs hand stats from the RotoWire player page, get t
        :param rotowire_id: the RotoWire unique ID of this player
        :param pitcher_hand: a str representation of the hand the pitcher throws with ("L" or "R")
        :return: a PregameHitterGameEntry object without the predicted_draftkings_points field populated
        """
        hitter_soup = BeautifulSoupHelper.get_soup_from_url(RotoWire.PLAYER_PAGE_BASE_URL + str(rotowire_id))
        pregame_hitter_entry = PregameHitterGameEntry()
        pregame_hitter_entry.rotowire_id = rotowire_id
        pregame_hitter_entry.team = team

        # Career stats
        try:
            career_table_row = hitter_soup.find("div", {"id": RotoWire.YEAR_TABLE_LABEL}).find("a", {"href": "/baseball/plcareer.htm?id=" + str(rotowire_id)}).parent.parent.parent
            career_table_entries = career_table_row.findAll("td")
            pregame_hitter_entry.career_ab = RotoWire.table_entry_to_int(career_table_entries[6].text)
            pregame_hitter_entry.career_r = RotoWire.table_entry_to_int(career_table_entries[7].text)
            pregame_hitter_entry.career_h = RotoWire.table_entry_to_int(career_table_entries[8].text)
            pregame_hitter_entry.career_hr = RotoWire.table_entry_to_int(career_table_entries[12].text)
            pregame_hitter_entry.career_rbi = RotoWire.table_entry_to_int(career_table_entries[13].text)
            pregame_hitter_entry.career_sb = RotoWire.table_entry_to_int(career_table_entries[14].text)
            pregame_hitter_entry.career_cs = RotoWire.table_entry_to_int(career_table_entries[15].text)
            pregame_hitter_entry.career_bb = RotoWire.table_entry_to_int(career_table_entries[16].text)
            pregame_hitter_entry.career_so = RotoWire.table_entry_to_int(career_table_entries[17].text)
        # Rotowire doesn't have the career table row, we have to add the stats over the years together
        except AttributeError:
            print "RotoWire does not have the career stats for %s." % RotoWire.get_name_from_id(rotowire_id)
            table_entries = hitter_soup.find("table", {"class": "tablesorter basicstats"}).find("tbody").findAll("td", {"class": "mlbstat-year"})
            for table_entry in table_entries:
                career_table_entries = table_entry.parent.findAll("td")
                if career_table_entries[2].text.strip() == "MAJ":
                    pregame_hitter_entry.career_ab += RotoWire.table_entry_to_int(career_table_entries[6].text)
                    pregame_hitter_entry.career_r += RotoWire.table_entry_to_int(career_table_entries[7].text)
                    pregame_hitter_entry.career_h += RotoWire.table_entry_to_int(career_table_entries[8].text)
                    pregame_hitter_entry.career_hr += RotoWire.table_entry_to_int(career_table_entries[12].text)
                    pregame_hitter_entry.career_rbi += RotoWire.table_entry_to_int(career_table_entries[13].text)
                    pregame_hitter_entry.career_sb += RotoWire.table_entry_to_int(career_table_entries[14].text)
                    pregame_hitter_entry.career_cs += RotoWire.table_entry_to_int(career_table_entries[15].text)
                    pregame_hitter_entry.career_bb += RotoWire.table_entry_to_int(career_table_entries[16].text)
                    pregame_hitter_entry.career_so += RotoWire.table_entry_to_int(career_table_entries[17].text)

        # Last 14 day stats
        special_stat_rows = hitter_soup.find("div", {"id": RotoWire.RECENT_TABLE_LABEL}).findAll("tr", {"class": "statrow-special"})
        for table_row in special_stat_rows:
            if table_row.find("td", {"class": RotoWire.TABLE_ENTRY_LABEL}).text == "Last 14 Days":
                recent_table_entries = table_row.findAll("td")
                pregame_hitter_entry.recent_ab = RotoWire.table_entry_to_int(recent_table_entries[2].text)
                pregame_hitter_entry.recent_r = RotoWire.table_entry_to_int(recent_table_entries[3].text)
                pregame_hitter_entry.recent_h = RotoWire.table_entry_to_int(recent_table_entries[4].text)
                pregame_hitter_entry.recent_hr = RotoWire.table_entry_to_int(recent_table_entries[7].text)
                pregame_hitter_entry.recent_rbi = RotoWire.table_entry_to_int(recent_table_entries[8].text)
                pregame_hitter_entry.recent_sb = RotoWire.table_entry_to_int(recent_table_entries[11].text)
                pregame_hitter_entry.recent_cs = RotoWire.table_entry_to_int(recent_table_entries[12].text)
                pregame_hitter_entry.recent_bb = RotoWire.table_entry_to_int(recent_table_entries[9].text)
                pregame_hitter_entry.recent_so = RotoWire.table_entry_to_int(recent_table_entries[10].text)
                break

        #Season stats
        hitter_soup = BeautifulSoupHelper.get_soup_from_url(RotoWire.BATTER_SPLIT_BASE_URL + str(rotowire_id))
        tables = hitter_soup.findAll("table", {"class": RotoWire.SPLIT_TABLE_LABEL})
        for table in tables:
            if table.find("td", {"class": "mlb-splitstats-sitheader"}).text == "Total":
                season_table_entries = table.find("tbody").findAll("td")
                pregame_hitter_entry.season_ab = RotoWire.table_entry_to_int(season_table_entries[1].text)
                pregame_hitter_entry.season_r = RotoWire.table_entry_to_int(season_table_entries[2].text)
                pregame_hitter_entry.season_h = RotoWire.table_entry_to_int(season_table_entries[3].text)
                pregame_hitter_entry.season_hr = RotoWire.table_entry_to_int(season_table_entries[7].text)
                pregame_hitter_entry.season_rbi = RotoWire.table_entry_to_int(season_table_entries[8].text)
                pregame_hitter_entry.season_bb = RotoWire.table_entry_to_int(season_table_entries[9].text)
                pregame_hitter_entry.season_so = RotoWire.table_entry_to_int(season_table_entries[10].text)
                pregame_hitter_entry.season_sb = RotoWire.table_entry_to_int(season_table_entries[11].text)
                pregame_hitter_entry.season_cs = RotoWire.table_entry_to_int(season_table_entries[12].text)
                break

        # Vs hand of the opposing pitcher
        if pitcher_hand == "L":
            pitcher_string = "vs Left"
        elif pitcher_hand == "R":
            pitcher_string = "vs Right"
        else:
            print "Invalid pitcher hand %i" % pitcher_hand
            assert 0
        for table in tables:
            if table.find("td", {"class": "mlb-splitstats-sitheader"}).text == "vs Pitcher":
                table_rows = table.find("tbody").findAll("tr")
                for table_row in table_rows:
                    #TODO: this shouldn't assume we will find an entry matching these parameters
                    #TODO: these are season vs numbers, we want career
                    if table_row.find("td", {"class": RotoWire.TABLE_ENTRY_LABEL}).text == pitcher_string:
                        vs_hand_table_entries = table_row.findAll("td")
                        pregame_hitter_entry.vs_hand_ab = RotoWire.table_entry_to_int(vs_hand_table_entries[1].text)
                        pregame_hitter_entry.vs_hand_r = RotoWire.table_entry_to_int(vs_hand_table_entries[2].text)
                        pregame_hitter_entry.vs_hand_h = RotoWire.table_entry_to_int(vs_hand_table_entries[3].text)
                        pregame_hitter_entry.vs_hand_hr = RotoWire.table_entry_to_int(vs_hand_table_entries[7].text)
                        pregame_hitter_entry.vs_hand_rbi = RotoWire.table_entry_to_int(vs_hand_table_entries[8].text)
                        pregame_hitter_entry.vs_hand_bb = RotoWire.table_entry_to_int(vs_hand_table_entries[9].text)
                        pregame_hitter_entry.vs_hand_so = RotoWire.table_entry_to_int(vs_hand_table_entries[10].text)
                        pregame_hitter_entry.vs_hand_sb = RotoWire.table_entry_to_int(vs_hand_table_entries[11].text)
                        pregame_hitter_entry.vs_hand_cs = RotoWire.table_entry_to_int(vs_hand_table_entries[12].text)
                        break
                break

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
