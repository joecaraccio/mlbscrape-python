
import unittest
from mlbscrape_python.mine.draft_kings import Draftkings


class GetSalariesTest(unittest.TestCase):
    """ Test case for testing the methods of getting the salaries for Draftkings
    """
    def pitcher_typical_test(self):
        CSV_LOCATION = "players.csv"
        NAME = "Felix Hernandez"
        TEAM = "Sea"

        csv_dict = Draftkings.get_csv_dict(CSV_LOCATION)
        try:
            csv_entry = csv_dict[NAME.lower() + TEAM.lower()]
        except KeyError:
            self.assertTrue(False)

        self.assertEqual(int(csv_entry["Salary"]), 10400)

    def hitter_typical_test(self):
        CSV_LOCATION = "players.csv"
        NAME = "Jon Jay"
        TEAM = "SD"

        csv_dict = Draftkings.get_csv_dict(CSV_LOCATION)
        try:
            csv_entry = csv_dict[NAME.lower() + TEAM.lower()]
        except KeyError:
            self.assertTrue(False)

        self.assertEqual(int(csv_entry["Salary"]), 2700)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(GetSalariesTest('pitcher_typical_test'))
    test_suite.addTest(GetSalariesTest('hitter_typical_test'))
    return test_suite