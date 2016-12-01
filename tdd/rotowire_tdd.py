
import unittest
from mine.rotowire import *
from mine.beautiful_soup_helper import *


class GetGamesTest(unittest.TestCase):
    HTML_LOCATION = "rotowire_lineups_partial.htm"
    DB_PATH = "test_db.db"

    def runTest(self):
        db = MlbDatabase(GetGamesTest.DB_PATH).open_session()
        games = get_game_lineups(GetGamesTest.DB_PATH, GetGamesTest.HTML_LOCATION)
        player = games[0].away_lineup[0]
        player_comparison = PlayerStruct('Logan Forsythe', 'TB', '10532', '2B', 'R')
        self.assertEqual(player, player_comparison)

        player = games[0].away_lineup[1]
        player_comparison = PlayerStruct('Logan Morrison', 'TB', '10427', '1B', 'L')
        self.assertEqual(player, player_comparison)

        player = games[0].away_pitcher
        player_comparison = PlayerStruct('Blake Snell', 'TB', '12189', 'P', 'L')
        self.assertEqual(player, player_comparison)

        player = games[0].home_lineup[0]
        player_comparison = PlayerStruct('Jacoby Ellsbury', 'NYY', '8635', 'CF', 'L')
        self.assertEqual(player, player_comparison)

        player = games[0].home_lineup[8]
        player_comparison = PlayerStruct('Didi Gregorius', 'NYY', '11257', 'SS', 'L')
        self.assertEqual(player, player_comparison)

        player = games[0].home_pitcher
        player_comparison = PlayerStruct('Masahiro Tanaka', 'NYY', '10879', 'P', 'R')
        self.assertEqual(player, player_comparison)

        player = games[1].home_pitcher
        player_comparison = PlayerStruct('Tanner Roark', 'WAS', '11929', 'P', 'R')
        self.assertEqual(player, player_comparison)

        player = games[1].home_lineup[0]
        player_comparison = PlayerStruct('Chris Heisey', 'WAS', '10920', 'CF', 'R')
        self.assertEqual(player, player_comparison)


class GetWindSpeedTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION_ZERO = "cubs_phillies_lineup.htm"
    HTML_LOCATION_POSITIVE = "jays_tigers_lineup.htm"
    HTML_LOCATION_NEGATIVE = "astros_rangers_lineup.htm"

    def test_typical_zero(self):
        soup = get_soup_from_url(GetWindSpeedTest.HTML_LOCATION_ZERO)
        wind_speed = get_wind_speed(soup)
        self.assertEqual(wind_speed, 0)

    def test_typical_positive(self):
        soup = get_soup_from_url(GetWindSpeedTest.HTML_LOCATION_POSITIVE)
        wind_speed = get_wind_speed(soup)
        self.assertEqual(wind_speed, 11)

    def test_typical_negative(self):
        soup = get_soup_from_url(GetWindSpeedTest.HTML_LOCATION_NEGATIVE)
        wind_speed = get_wind_speed(soup)
        self.assertEqual(wind_speed, -9)


class GetUmpKsTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION = "cubs_phillies_lineup.htm"

    def test_typical_zero(self):
        soup = get_soup_from_url(GetUmpKsTest.HTML_LOCATION)
        ump_ks = get_ump_ks_per_game(soup)
        self.assertEqual(ump_ks, 15.75)


class GetUmpRunsTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION = "cubs_phillies_lineup.htm"

    def test_typical_zero(self):
        soup = get_soup_from_url(GetUmpRunsTest.HTML_LOCATION)
        ump_runs = get_ump_runs_per_game(soup)
        self.assertEqual(ump_runs, 10.98)


def suite():
    test_suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(GetWindSpeedTest),
                                     unittest.TestLoader().loadTestsFromTestCase(GetUmpKsTest)])
    test_suite.addTest(GetGamesTest())
    return test_suite