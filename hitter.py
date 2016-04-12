from player import Player


class Hitter(Player):
    """ A class housing stats for hitters
    :param first_name: First name of the Hitter
    :param last_name: Last name of the Hitter
    :param id: unique MLB ID
    :param team: abbreviation of the Hitter's team
    :param batting_order: the integer place in the batting order for this Hitter
    :param batting_hand: left, right, or switch
    """
    def __init__(self, first_name, last_name, pitchfx_id, baseball_ref_id, team, batting_order, batting_hand):
        super(Hitter, self).__init__(first_name, last_name, pitchfx_id, baseball_ref_id, team, batting_hand)
        self.batting_order = int(batting_order)

    def set_game_results(self, game_id, soup_node):
        """ Mine the mlb.com boxscore XML file for the actual results of the game
        :param game_id: The unique ID for the MLB game
        :param soup_node: The BeautifulSoup XML node for the game results
        """
        self.game_id = str(game_id)
        self.game_date = Player.game_id_to_date(game_id)
        self.game_ab = float(soup_node.get("ab"))
        self.game_h = float(soup_node.get("h"))
        self.game_2b = float(soup_node.get("d"))
        self.game_3b = float(soup_node.get("t"))
        self.game_hbp = float(soup_node.get("hbp"))
        self.game_bb = float(soup_node.get("bb"))
        self.game_so = float(soup_node.get("so"))
        self.game_r = float(soup_node.get("r"))
        self.game_sb = float(soup_node.get("sb"))
        self.game_cs = float(soup_node.get("cs"))
        self.game_hr = float(soup_node.get("hr"))
        self.game_rbi = float(soup_node.get("rbi"))
        self.calculate_draftkings_points()

    def set_season_stats(self, soup):
        """ Mine the mlb.com batter XML file and set the season members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        season_stat_node = soup.find("season")
        if season_stat_node is not None:
            self.season_ab = float(season_stat_node.get("ab")) - self.game_ab
            self.season_h = float(season_stat_node.get("h")) - self.game_h
            self.season_bb = float(season_stat_node.get("bb")) - self.game_bb
            self.season_so = float(season_stat_node.get("so")) - self.game_so
            self.season_r = float(season_stat_node.get("r")) - self.game_r
            self.season_sb = float(season_stat_node.get("sb")) - self.game_sb
            self.season_cs = float(season_stat_node.get("cs")) - self.game_cs
            self.season_hr = float(season_stat_node.get("hr")) - self.game_hr
            self.season_rbi = float(season_stat_node.get("rbi")) - self.game_rbi

    def set_career_stats(self, soup):
        """ Mine the mlb.com batter XML file and set the career members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        career_stat_node = soup.find("career")
        if career_stat_node is not None:
            self.career_ab = float(career_stat_node.get("ab")) - self.game_ab
            self.career_h = float(career_stat_node.get("h")) - self.game_h
            self.career_bb = float(career_stat_node.get("bb")) - self.game_bb
            self.career_so = float(career_stat_node.get("so")) - self.game_so
            self.career_r = float(career_stat_node.get("r"))  - self.game_r
            self.career_sb = float(career_stat_node.get("sb")) - self.game_sb
            self.career_cs = float(career_stat_node.get("cs")) - self.game_cs
            self.career_hr = float(career_stat_node.get("hr")) - self.game_hr
            self.career_rbi = float(career_stat_node.get("rbi")) - self.game_rbi

    def set_vs_stats(self, vs_stats, vs_hand_stats, year):
        """ Mine the mlb.com batter XML file and set the vs members
        :param soup: The BeautifulSoup XML object for the batter XML file
        Note: For some reason, these stats don't follow the convention of including the results from the game.
        """
        if vs_stats is not None:
            self.vs_ab = float(vs_stats.ab)
            self.vs_h = float(vs_stats.h)
            self.vs_bb = float(vs_stats.bb)
            self.vs_so = float(vs_stats.so)
            self.vs_hr = float(vs_stats.hr)
            self.vs_rbi = float(vs_stats.rbi)
            
        # Versus left handed pitching
        if vs_hand_stats is not None:
            self.vs_hand_ab = float(vs_hand_stats.ab)
            self.vs_hand_h = float(vs_hand_stats.h)
            self.vs_hand_bb = float(vs_hand_stats.bb)
            self.vs_hand_so = float(vs_hand_stats.so)
            self.vs_hand_r = float(vs_hand_stats.r)
            self.vs_hand_sb = float(vs_hand_stats.sb)
            self.vs_hand_cs = float(vs_hand_stats.cs)
            self.vs_hand_hr = float(vs_hand_stats.hr)
            self.vs_hand_rbi = float(vs_hand_stats.rbi)

    def set_month_stats(self, soup):
        """ # Mine the mlb.com batter XML file and set the month members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        vs_stat_node = soup.find("month")
        if vs_stat_node is not None:
            self.month_ab = float(vs_stat_node.get("ab")) - self.game_ab
            self.month_h = float(vs_stat_node.get("h")) - self.game_h
            self.month_bb = float(vs_stat_node.get("bb")) - self.game_bb
            self.month_so = float(vs_stat_node.get("so")) - self.game_so
            self.month_r = float(vs_stat_node.get("r")) - self.game_r
            self.month_sb = float(vs_stat_node.get("sb")) - self.game_sb
            self.month_cs = float(vs_stat_node.get("cs")) - self.game_cs
            self.month_hr = float(vs_stat_node.get("hr")) - self.game_hr
            self.month_rbi = float(vs_stat_node.get("rbi")) - self.game_rbi

    def calculate_draftkings_points(self):
        """ Calculate the DraftKings points from the game results
        """
        self.draftkings_points = 3 * (self.game_h - self.game_2b - self.game_3b - self.game_hr)
        self.draftkings_points += 5*self.game_2b
        self.draftkings_points += 8*self.game_3b
        self.draftkings_points += 10*self.game_hr
        self.draftkings_points += 2*self.game_rbi
        self.draftkings_points += 2*self.game_r
        self.draftkings_points += 2*self.game_bb
        self.draftkings_points += 2*self.game_hbp
        self.draftkings_points += 5*self.game_sb
        self.draftkings_points -= 2*self.game_cs
