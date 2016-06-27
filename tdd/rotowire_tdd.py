
import unittest
import mine.rotowire
from mine.beautiful_soup_helper import BeautifulSoupHelper
from datetime import date, timedelta


class GetWindSpeedTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION_ZERO = "cubs_phillies_lineup.htm"
    HTML_LOCATION_POSITIVE = "jays_tigers_lineup.htm"
    HTML_LOCATION_NEGATIVE = "astros_rangers_lineup.htm"

    def test_typical_zero(self):
        soup = BeautifulSoupHelper.get_soup_from_url(GetWindSpeedTest.HTML_LOCATION_ZERO)
        wind_speed = get_wind_speed(soup)
        self.assertEqual(wind_speed, 0)

    def test_typical_positive(self):
        soup = BeautifulSoupHelper.get_soup_from_url(GetWindSpeedTest.HTML_LOCATION_POSITIVE)
        wind_speed = RotoWire.get_wind_speed(soup)
        self.assertEqual(wind_speed, 11)

    def test_typical_negative(self):
        soup = BeautifulSoupHelper.get_soup_from_url(GetWindSpeedTest.HTML_LOCATION_NEGATIVE)
        wind_speed = RotoWire.get_wind_speed(soup)
        self.assertEqual(wind_speed, -9)


class GetUmpKsTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION = "cubs_phillies_lineup.htm"

    def test_typical_zero(self):
        soup = BeautifulSoupHelper.get_soup_from_url(GetUmpKsTest.HTML_LOCATION)
        ump_ks = RotoWire.get_ump_ks_per_game(soup)
        self.assertEqual(ump_ks, 15.75)


class GetUmpRunsTest(unittest.TestCase):
    """ Test case for testing the get_hitter_id function
    """
    HTML_LOCATION = "cubs_phillies_lineup.htm"

    def test_typical_zero(self):
        soup = BeautifulSoupHelper.get_soup_from_url(GetUmpRunsTest.HTML_LOCATION)
        ump_runs = RotoWire.get_ump_runs_per_game(soup)
        self.assertEqual(ump_runs, 10.98)


def suite():
    test_suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(GetWindSpeedTest),
                                     unittest.TestLoader().loadTestsFromTestCase(GetUmpKsTest)])
    return test_suite