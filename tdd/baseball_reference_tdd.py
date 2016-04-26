
import unittest
from mlbscrape_python.mine.baseball_reference import BaseballReference
from mlbscrape_python.mine.beautiful_soup_helper import BeautifulSoupHelper


class GetHitterIdTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION = "baseball_reference_batting_2016.shtml"

    def setUp(self):
        self.soup = BeautifulSoupHelper.get_soup_from_url(GetHitterIdTest.HTML_LOCATION)

    def typical_test(self):
        hitter_id = BaseballReference.get_hitter_id("Dustin Pedroia",
                                                    "BOS",
                                                    "2016",
                                                    self.soup)
        self.assertEqual(hitter_id, "pedrodu01")

    def wrong_team_test(self):
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

    def typical_test(self):
        hitter_id = BaseballReference.get_pitcher_id("Matt Barnes",
                                                     "BOS",
                                                     "2016",
                                                     self.soup)
        self.assertEqual(hitter_id, "barnema01")

    def wrong_team_test(self):
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
    def career_typical_test(self):
        HTML_LOCATION = "career_stats_beltran.html"
        ID = "beltrca01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_career_hitting_stats(ID, soup)
        self.assertEqual(career_stats.ab, 8810)
        self.assertEqual(career_stats.r, 1459)
        self.assertEqual(career_stats.h, 2471)
        self.assertEqual(career_stats.hr, 396)
        self.assertEqual(career_stats.rbi, 1452)
        self.assertEqual(career_stats.sb, 311)
        self.assertEqual(career_stats.bb, 1018)
        self.assertEqual(career_stats.so, 1608)

    def recent_typical_test(self):
        HTML_LOCATION = "career_stats_pedroia.html"
        ID = "pedrodu01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_recent_hitting_stats(ID, soup)
        self.assertEqual(career_stats.ab, 48)
        self.assertEqual(career_stats.r, 8)
        self.assertEqual(career_stats.h, 14)
        self.assertEqual(career_stats.hr, 1)
        self.assertEqual(career_stats.rbi, 4)
        self.assertEqual(career_stats.sb, 0)
        self.assertEqual(career_stats.bb, 3)
        self.assertEqual(career_stats.so, 10)

    def vs_hand_typical_test(self):
        HTML_LOCATION = "career_stats_pedroia.html"
        ID = "pedrodu01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_vs_hand_hitting_stats(ID, BaseballReference.HandEnum.LHP, soup)
        self.assertEqual(career_stats.ab, 1394)
        self.assertEqual(career_stats.r, 232)
        self.assertEqual(career_stats.h, 425)
        self.assertEqual(career_stats.hr, 31)
        self.assertEqual(career_stats.rbi, 149)
        self.assertEqual(career_stats.sb, 42)
        self.assertEqual(career_stats.bb, 190)
        self.assertEqual(career_stats.so, 151)

    def season_typical_test(self):
        HTML_LOCATION = "stats_pedroia_2016.html"
        ID = "pedrodu01"
        YEAR = "2016"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        season_stats = BaseballReference.get_season_hitting_stats(ID, YEAR, soup)
        self.assertEqual(season_stats.ab, 67)
        self.assertEqual(season_stats.r, 11)
        self.assertEqual(season_stats.h, 20)
        self.assertEqual(season_stats.hr, 1)
        self.assertEqual(season_stats.rbi, 6)
        self.assertEqual(season_stats.sb, 0)
        self.assertEqual(season_stats.bb, 4)
        self.assertEqual(season_stats.so, 12)

    def vs_pitcher_typical_test(self):
        HTML_LOCATION = "stats_pedroia_vs_sabathia.html"
        ID = "pedrodu01"
        PITCHER_ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        vs_stats = BaseballReference.get_vs_pitcher_stats(ID, PITCHER_ID, soup)
        self.assertEqual(vs_stats.ab, 61)
        self.assertEqual(vs_stats.h, 17)
        self.assertEqual(vs_stats.hr, 0)
        self.assertEqual(vs_stats.rbi, 3)
        self.assertEqual(vs_stats.bb, 6)
        self.assertEqual(vs_stats.so, 15)


class GetPitchingStats(unittest.TestCase):
    """ Test case for testing the methods of getting pitching stats
    """

    def career_typical_test(self):
        HTML_LOCATION = "career_stats_sabathia.html"
        ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        career_stats = BaseballReference.get_career_pitching_stats(ID, soup)
        self.assertEqual(career_stats.wins, 215)
        self.assertEqual(career_stats.losses, 130)
        self.assertEqual(career_stats.batters_faced, 12538)
        self.assertEqual(career_stats.ip, 3004.0)
        self.assertEqual(career_stats.hr, 294)
        self.assertEqual(career_stats.bb, 902)
        self.assertEqual(career_stats.so, 2584)

    def recent_typical_test(self):
        HTML_LOCATION = "career_stats_sabathia.html"
        ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        recent_stats = BaseballReference.get_recent_pitcher_stats(ID, soup)
        self.assertEqual(recent_stats.wins, 0)
        self.assertEqual(recent_stats.losses, 1)
        self.assertEqual(recent_stats.batters_faced, 48)
        self.assertEqual(recent_stats.ip, 9.1)
        self.assertEqual(recent_stats.hr, 1)
        self.assertEqual(recent_stats.bb, 4)
        self.assertEqual(recent_stats.so, 7)

    def season_typical_test(self):
        HTML_LOCATION = "stats_sabathia_2016.html"
        ID = "sabatc.01"
        YEAR = "2016"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        season_stats = BaseballReference.get_season_pitcher_stats(ID, YEAR, soup)
        self.assertEqual(season_stats.wins, 1)
        self.assertEqual(season_stats.losses, 1)
        self.assertEqual(season_stats.batters_faced, 73)
        self.assertEqual(season_stats.ip, 15.1)
        self.assertEqual(season_stats.hr, 1)
        self.assertEqual(season_stats.bb, 8)
        self.assertEqual(season_stats.so, 10)
"""
    def vs_pitcher_typical_test(self):
        HTML_LOCATION = "stats_pedroia_vs_sabathia.html"
        ID = "pedrodu01"
        PITCHER_ID = "sabatc.01"
        soup = BeautifulSoupHelper.get_soup_from_url(HTML_LOCATION)
        vs_stats = BaseballReference.get_vs_pitcher_stats(ID, PITCHER_ID, soup)
        self.assertEqual(vs_stats.ab, 61)
        self.assertEqual(vs_stats.h, 17)
        self.assertEqual(vs_stats.hr, 0)
        self.assertEqual(vs_stats.rbi, 3)
        self.assertEqual(vs_stats.bb, 6)
        self.assertEqual(vs_stats.so, 15)
    """

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(GetHitterIdTest('typical_test'))
    test_suite.addTest(GetHitterIdTest('wrong_team_test'))
    test_suite.addTest(GetPitcherIdTest('typical_test'))
    test_suite.addTest(GetPitcherIdTest('wrong_team_test'))
    test_suite.addTest(GetHittingStats('career_typical_test'))
    test_suite.addTest(GetHittingStats('recent_typical_test'))
    test_suite.addTest(GetHittingStats('vs_hand_typical_test'))
    test_suite.addTest(GetHittingStats('season_typical_test'))
    test_suite.addTest(GetHittingStats('vs_pitcher_typical_test'))
    test_suite.addTest(GetPitchingStats('career_typical_test'))
    test_suite.addTest(GetPitchingStats('recent_typical_test'))
    test_suite.addTest(GetPitchingStats('season_typical_test'))
    #test_suite = unittest.TestLoader().loadTestsFromTestCase(GetHitterIdTest)
    return test_suite