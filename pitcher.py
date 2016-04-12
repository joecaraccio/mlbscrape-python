from player import Player


class Pitcher(Player):
    def __init__(self, first_name, last_name, pitchfx_id, baseball_reference_id, team, pitching_hand):
        """ A class housing stats for pitchers
        :param first_name: first name of the pitcher
        :param last_name: last name of the pitcher
        :param id: Pitch FX ID of the pitcher
        :param team: team abbrevation of the pitcher
        :param pitching_hand: right or left handed pitcher
        """
        super(Pitcher, self).__init__(first_name, last_name, pitchfx_id, baseball_reference_id, team, pitching_hand)

    def set_game_results(self, game_id, soup_node):
        """ # Mine the mlb.com boxscore XML file for the actual results of the game
        :param game_id: The unique ID for the MLB game
        :param soup_node: The BeautifulSoup XML node for the game results
        """
        self.game_id = str(game_id)
        self.game_date = Player.game_id_to_date(game_id)
        self.game_outs = int(soup_node.get("out"))
        self.game_so = int(soup_node.get("so"))
        self.game_wins = 0
        if soup_node.has_attr("win"):
            if str(soup_node.get("win")) == "true":
                self.game_wins = 1
        self.game_losses = 0
        if soup_node.has_attr("loss"):
            if str(soup_node.get("loss")) == "true":
                self.game_losses = 1
        self.game_er = int(soup_node.get("er"))
        self.game_h = int(soup_node.get("h"))
        self.game_bb = int(soup_node.get("bb"))
        self.game_hr = int(soup_node.get("hr"))
        # TODO: it is possible to throw a complete game and lose and get less than 27 outs
        if self.game_outs == 27:
            self.game_cg = 1
        else:
            self.game_cg = 0
        if self.game_cg == 1:
            if int(soup_node.get("r")) == 0:
                self.game_cg_shutout = 1
            else:
                self.game_cg_shutout = 0
        else:
            self.game_cg_shutout = 0
        if self.game_outs == 27 and self.game_h == 0:
            self.game_no_hitter = 1
        else:
            self.game_no_hitter = 0
            
        self.calculate_draftkings_points()

    def set_season_stats(self, soup):
        """ Mine the mlb.com batter XML file and set the season members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        season_stat_node = soup.find("season")
        if season_stat_node is not None:
            innings_string = season_stat_node.get("ip")
            self.season_outs = Player.inning_str_to_outs(innings_string) - self.game_outs
            self.season_so = int(season_stat_node.get("so")) - self.game_so
            self.season_wins = int(season_stat_node.get("w"))
            self.season_losses = int(season_stat_node.get("l"))
            season_and_game_innings = Player.inning_str_to_float(innings_string)
            try:
                season_era = float(season_stat_node.get("era"))
            except ValueError:
                season_era = 0.0
            self.season_er = Player.era_to_er(season_era, season_and_game_innings) - self.game_er
            self.season_h = int(season_stat_node.get("h")) - self.game_h
            self.season_bb = int(season_stat_node.get("bb")) - self.game_bb
            self.season_hr = int(season_stat_node.get("hr")) - self.game_hr

    def set_career_stats(self,soup):
        """ Mine the mlb.com batter XML file and set the career members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        career_stat_node = soup.find("career")
        if career_stat_node is not None:
            innings_string = career_stat_node.get("ip")
            self.career_outs = Player.inning_str_to_outs(innings_string) - self.game_outs
            self.career_so = int(career_stat_node.get("so")) - self.game_so
            self.career_wins = int(career_stat_node.get("w"))
            self.career_losses = int(career_stat_node.get("l"))
            career_and_game_innings = Player.inning_str_to_float(innings_string)
            try:
                career_era = float(career_stat_node.get("era"))
            except ValueError:
                career_era = 0.0
            self.career_er = Player.era_to_er(career_era, career_and_game_innings) - self.game_er
            self.career_h = int(career_stat_node.get("h")) - self.game_h
            self.career_bb = int(career_stat_node.get("bb")) - self.game_bb
            self.career_hr = int(career_stat_node.get("hr")) - self.game_hr

    def set_vs_stats(self, soup):
        """ Mine the mlb.com batter XML file and set the vs members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        # Versus this team
        vs_stat_node = soup.find("team")
        if vs_stat_node is not None:
            innings_string = vs_stat_node.get("ip")
            self.vs_outs = Player.inning_str_to_outs(innings_string) - self.game_outs
            self.vs_so = int(vs_stat_node.get("so")) - self.game_so
            vs_and_game_innings = Player.inning_str_to_float(innings_string)
            try:
                vs_era = float(vs_stat_node.get("era"))
            except ValueError:
                vs_era = 0.0
            self.vs_er = Player.era_to_er(vs_era, vs_and_game_innings) - self.game_er
            self.vs_h = int(vs_stat_node.get("h")) - self.game_h
            self.vs_bb = int(vs_stat_node.get("bb")) - self.game_bb
            self.vs_hr = int(vs_stat_node.get("hr")) - self.game_hr
            
        # Versus left handed hitters
        vs_stat_node = soup.find("vs_lhb")
        if vs_stat_node is not None:
            innings_string = vs_stat_node.get("ip")
            self.vs_lhb_outs = Player.inning_str_to_outs(innings_string) - self.game_outs
            self.vs_lhb_so = float(vs_stat_node.get("so"))
            vs_and_game_innings = Player.inning_str_to_float(innings_string)
            try:
                vs_lhb_era = float(vs_stat_node.get("era"))
            except ValueError:
                vs_lhb_era = 0.0
            self.vs_lhb_er = Player.era_to_er(vs_lhb_era, vs_and_game_innings) - self.game_er
            self.vs_lhb_ab = float(vs_stat_node.get("ab"))
            self.vs_lhb_h = float(vs_stat_node.get("h"))
            self.vs_lhb_bb = float(vs_stat_node.get("bb"))
            self.vs_lhb_hr = float(vs_stat_node.get("hr"))
            
        # Versus right handed hitters
        vs_stat_node = soup.find("vs_rhb")
        if vs_stat_node is not None:
            innings_string = vs_stat_node.get("ip")
            self.vs_rhb_outs = Player.inning_str_to_outs(innings_string) - self.game_outs
            self.vs_rhb_so = float(vs_stat_node.get("so"))
            vs_and_game_innings = Player.inning_str_to_float(innings_string)
            try:
                vs_rhb_era = float(vs_stat_node.get("era"))
            except ValueError:
                vs_rhb_era = 0.0
            self.vs_rhb_er = Player.era_to_er(vs_rhb_era, vs_and_game_innings) - self.game_er
            self.vs_rhb_ab = float(vs_stat_node.get("ab"))
            self.vs_rhb_h = float(vs_stat_node.get("h"))
            self.vs_rhb_bb = float(vs_stat_node.get("bb"))
            self.vs_rhb_hr = float(vs_stat_node.get("hr"))

    def set_month_stats(self, soup):
        """ Mine the mlb.com batter XML file and set the month members
        :param soup: The BeautifulSoup XML object for the batter XML file
        """
        vs_stat_node = soup.find("month")
        if vs_stat_node is not None:
            innings_string = vs_stat_node.get("ip")
            self.month_outs = Player.inning_str_to_outs(innings_string) - self.game_outs
            self.month_so = int(vs_stat_node.get("so")) - self.game_so
            vs_and_month_innings = Player.inning_str_to_float(innings_string)
            try:
                month_era = float(vs_stat_node.get("era"))
            except ValueError:
                month_era = 0.0
            self.month_er = Player.era_to_er(month_era, vs_and_month_innings) - self.game_er
            self.month_h = int(vs_stat_node.get("h")) - self.game_h
            self.month_bb = int(vs_stat_node.get("bb")) - self.game_bb
            self.month_hr = int(vs_stat_node.get("hr")) - self.game_hr
    
    # Calculate the DraftKings points from the game results    
    def calculate_draftkings_points(self):
        self.draft_kings_points = 2.25*(float(self.game_outs) / 3)
        self.draft_kings_points += 2*self.game_so
        self.draft_kings_points += 5*self.game_wins
        self.draft_kings_points -= 2*self.game_er
        self.draft_kings_points -= 0.6*self.game_h
        self.draft_kings_points -= 0.6*self.game_bb
        # TODO: we may need to get HBP data from elsewhere
        #self.mTotalPoints -= 0.6*self.mGameHbp
        self.draft_kings_points += 2.5*self.game_cg
        self.draft_kings_points += 2.5*self.game_cg_shutout
        self.draft_kings_points += 5*self.game_no_hitter
        