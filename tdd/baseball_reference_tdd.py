
import unittest
from Released.mlbscrape_python.mine.baseball_reference import BaseballReference
from Released.mlbscrape_python.mine.beautiful_soup_helper import BeautifulSoupHelper
from datetime import date, timedelta

class GetHitterIdTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION = "baseball_reference_batting_2016.shtml"

    def setUp(self):
        self.soup = BeautifulSoupHelper.get_soup_from_url(GetHitterIdTest.HTML_LOCATION)

    def test_typical(self):
        hitter_id = BaseballReference.get_hitter_id("Dustin Pedroia",
                                                    "BOS",
                                                    "2016",
                                                    self.soup)
        self.assertEqual(hitter_id, "pedrodu01")

    def test_wrong_team(self):
        try:
            hitter_id = BaseballReference.get_hitter_id("Dustin Pedroia",
                                                    "TBR",
                                                    "2016",
                                                    self.soup)
            self.assertTrue(False)
        except BaseballReference.NameNotFound:
            self.assertTrue(True)


class GetPitcherIdTest(unittest.TestCase):
    """ Test case for testing the get_pitcher_id function
    """
    HTML_LOCATION = "baseball_reference_pitching_2016.shtml"

    def setUp(self):
        self.soup = BeautifulSoupHelper.get_soup_from_url(GetPitcherIdTest.HTML_LOCATION)

    def test_typical(self):
        hitter_id = BaseballReference.get_pitcher_id("Matt Barnes",
                                                     "BOS",
                                                     "2016",
                                                     self.soup)
        self.assertEqual(hitter_id, "barnema01")

    def test_wrong_team(self):
        try:
            hitter_id = BaseballReference.get_pitcher_id("Matt Barnes",
                                                    "TBR",
                                                    "2016",
                                                    self.soup)
            self.assertTrue(False)
        except BaseballReference.NameNotFound:
            self.assertTrue(True)


class GetHittingStats(unittest.TestCase):
    """ Test case for testing the methods of getting hitting stats
    """
    def test_career_typical(self):
        HTML_LOCATION = "career_stats_beltran.html"
        ID = "beltrca01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_career_hitting_stats(ID, soup)
        self.assertEqual(int(career_stats["AB"]), 8810)
        self.assertEqual(int(career_stats["R"]), 1459)
        self.assertEqual(int(career_stats["H"]), 2471)
        self.assertEqual(int(career_stats["HR"]), 396)
        self.assertEqual(int(career_stats["RBI"]), 1452)
        self.assertEqual(int(career_stats["SB"]), 311)
        self.assertEqual(int(career_stats["BB"]), 1018)
        self.assertEqual(int(career_stats["SO"]), 1608)

    def test_recent_typical(self):
        HTML_LOCATION = "career_stats_pedroia.html"
        ID = "pedrodu01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_recent_hitting_stats(ID, soup)
        self.assertEqual(int(career_stats["AB"]), 48)
        self.assertEqual(int(career_stats["R"]), 8)
        self.assertEqual(int(career_stats["H"]), 14)
        self.assertEqual(int(career_stats["HR"]), 1)
        self.assertEqual(int(career_stats["RBI"]), 4)
        self.assertEqual(int(career_stats["SB"]), 0)
        self.assertEqual(int(career_stats["BB"]), 3)
        self.assertEqual(int(career_stats["SO"]), 10)

    def test_vs_hand_typical(self):
        HTML_LOCATION = "career_stats_pedroia.html"
        ID = "pedrodu01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_vs_hand_hitting_stats(ID, BaseballReference.HandEnum.LHP, soup)
        self.assertEqual(int(career_stats["AB"]), 1394)
        self.assertEqual(int(career_stats["R"]), 232)
        self.assertEqual(int(career_stats["H"]), 425)
        self.assertEqual(int(career_stats["HR"]), 31)
        self.assertEqual(int(career_stats["RBI"]), 149)
        self.assertEqual(int(career_stats["SB"]), 42)
        self.assertEqual(int(career_stats["BB"]), 190)
        self.assertEqual(int(career_stats["SO"]), 151)

    def test_season_typical(self):
        HTML_LOCATION = "stats_pedroia_2016.html"
        ID = "pedrodu01"
        YEAR = "2016"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        season_stats = BaseballReference.get_season_hitting_stats(ID, YEAR, soup)
        self.assertEqual(int(season_stats["AB"]), 67)
        self.assertEqual(int(season_stats["R"]), 11)
        self.assertEqual(int(season_stats["H"]), 20)
        self.assertEqual(int(season_stats["HR"]), 1)
        self.assertEqual(int(season_stats["RBI"]), 6)
        self.assertEqual(int(season_stats["SB"]), 0)
        self.assertEqual(int(season_stats["BB"]), 4)
        self.assertEqual(int(season_stats["SO"]), 12)

    def test_vs_pitcher_typical(self):
        HTML_LOCATION = "stats_pedroia_vs_sabathia.html"
        ID = "pedrodu01"
        PITCHER_ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        vs_stats = BaseballReference.get_vs_pitcher_stats(ID, PITCHER_ID, soup)
        self.assertEqual(int(vs_stats["AB"]), 61)
        self.assertEqual(int(vs_stats["H"]), 17)
        self.assertEqual(int(vs_stats["HR"]), 0)
        self.assertEqual(int(vs_stats["RBI"]), 3)
        self.assertEqual(int(vs_stats["BB"]), 6)
        self.assertEqual(int(vs_stats["SO"]), 15)


class GetPitchingStats(unittest.TestCase):
    """ Test case for testing the methods of getting pitching stats
    """

    def test_career_typical(self):
        HTML_LOCATION = "career_stats_sabathia.html"
        ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_career_pitching_stats(ID, soup)
        self.assertEqual(int(career_stats["W"]), 215)
        self.assertEqual(int(career_stats["L"]), 130)
        self.assertEqual(int(career_stats["BF"]), 12538)
        self.assertEqual(float(career_stats["IP"]), 3004.0)
        self.assertEqual(int(career_stats["HR"]), 294)
        self.assertEqual(int(career_stats["BB"]), 902)
        self.assertEqual(int(career_stats["SO"]), 2584)

    def test_recent_typical(self):
        HTML_LOCATION = "career_stats_sabathia.html"
        ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        recent_stats = BaseballReference.get_recent_pitcher_stats(ID, soup)
        self.assertEqual(int(recent_stats["W"]), 0)
        self.assertEqual(int(recent_stats["L"]), 1)
        self.assertEqual(int(recent_stats["BF"]), 48)
        self.assertEqual(float(recent_stats["IP"]), 9.1)
        self.assertEqual(int(recent_stats["HR"]), 1)
        self.assertEqual(int(recent_stats["BB"]), 4)
        self.assertEqual(int(recent_stats["SO"]), 7)

    def test_season_typical(self):
        HTML_LOCATION = "stats_sabathia_2016.html"
        ID = "sabatc.01"
        YEAR = "2016"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        season_stats = BaseballReference.get_season_pitcher_stats(ID, YEAR, soup)
        self.assertEqual(int(season_stats["W"]), 1)
        self.assertEqual(int(season_stats["L"]), 1)
        self.assertEqual(int(season_stats["BF"]), 73)
        self.assertEqual(float(season_stats["IP"]), 15.1)
        self.assertEqual(int(season_stats["HR"]), 1)
        self.assertEqual(int(season_stats["BB"]), 8)
        self.assertEqual(int(season_stats["SO"]), 10)

    def test_yesterdays_game_typical(self):
        HTML_LOCATION = "game_log_steven_wright.html"
        ID = "wrighst01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        game_date = date(day=27, month=4, year=2016)
        game_stats = BaseballReference.get_pitching_game_log(ID, soup, game_date)
        self.assertEqual(float(game_stats["IP"]), 7.0)


class GetTeamInfoTest(unittest.TestCase):

    HTML_LOCATION = "padres_team_info.html"

    def runTest(self):
        team_soup = BeautifulSoupHelper.get_soup_from_url(GetTeamInfoTest.HTML_LOCATION)
        team_info = BaseballReference.get_team_info("San Diego Padres", 2016, team_soup)
        self.assertEqual(team_info.hitter_factor, 93)
        self.assertEqual(team_info.pitcher_factor, 94)


def suite():
    test_suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(GetHitterIdTest),
                 unittest.TestLoader().loadTestsFromTestCase(GetPitcherIdTest),
                 unittest.TestLoader().loadTestsFromTestCase(GetHittingStats),
                 unittest.TestLoader().loadTestsFromTestCase(GetPitchingStats)])
    test_suite.addTest(GetTeamInfoTest())
    return test_suite