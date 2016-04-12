
from beautiful_soup_helper import BeautifulSoupHelper


class RotoWire(object):

    # Relevant HTML we rely on
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

    class PlayerStruct(object):
        def __init__(self, name, team):
            self.name = name
            self.team = team

    @staticmethod
    def get_lineups():
        lineup_soup = BeautifulSoupHelper.get_soup_from_url(RotoWire.DAILY_LINEUPS_URL)
        header_nodes = lineup_soup.findAll("div", {"class": RotoWire.TEAM_REGION_LABEL})
        lineups = {}
        for header_node in header_nodes:
            game_node = header_node.parent
            home_team_lineup = {}
            away_team_lineup = {}
            away_team_abbreviation = game_node.find("div", {"class": RotoWire.AWAY_TEAM_REGION_LABEL}).text.split()[0]
            home_team_abbreviation = game_node.find("div", {"class": RotoWire.HOME_TEAM_REGION_LABEL}).text.split()[0]
            game_main_soup = game_node.find("div", {"class": RotoWire.LINEUPS_CLASS_LABEL})
            for away_player in game_main_soup.findAll("div", {"class": RotoWire.AWAY_TEAM_PLAYER_LABEL}):
                name = away_player.find("a").text
                position = away_player.find("div", {"class": RotoWire.POSITION_CLASS_LABEL}).text
                team = away_team_abbreviation
                away_team_lineup[position] = RotoWire.PlayerStruct(name, team)

            for home_player in game_main_soup.findAll("div", {"class": RotoWire.HOME_TEAM_PLAYER_LABEL}):
                name = home_player.find("a").text
                position = home_player.find("div", {"class": RotoWire.POSITION_CLASS_LABEL}).text
                team = home_team_abbreviation
                home_team_lineup[position] = RotoWire.PlayerStruct(name, team)

            pitchers = game_node.find("div", RotoWire.PITCHERS_REGION_LABEL).findAll("div")
            away_team_lineup["P"] = RotoWire.PlayerStruct(pitchers[0].find("a").text, away_team_abbreviation)
            home_team_lineup["P"] = RotoWire.PlayerStruct(pitchers[1].find("a").text, home_team_abbreviation)


