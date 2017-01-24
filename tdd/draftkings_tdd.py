
import unittest
from mine.draft_kings import *
from mine.stat_miner import *
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
import heapq


class OptimalLineupTest(unittest.TestCase):
    """ Base class used to initialize the optimal lineup before operating on it
    """
    OPTIMAL_LINEUP_SP1_ID = "1"
    OPTIMAL_LINEUP_SP1_SALARY = 1000
    OPTIMAL_LINEUP_SP1_POINTS = 23.5

    OPTIMAL_LINEUP_SP2_ID = "2"
    OPTIMAL_LINEUP_SP2_SALARY = 8500
    OPTIMAL_LINEUP_SP2_POINTS = 19.8

    OPTIMAL_LINEUP_C_ID = "3"
    OPTIMAL_LINEUP_C_SALARY = 3000
    OPTIMAL_LINEUP_C_POINTS = 8

    OPTIMAL_LINEUP_1B_ID = "4"
    OPTIMAL_LINEUP_1B_SALARY = 5800
    OPTIMAL_LINEUP_1B_POINTS = 12

    OPTIMAL_LINEUP_2B_ID = "5"
    OPTIMAL_LINEUP_2B_SALARY = 4800
    OPTIMAL_LINEUP_2B_POINTS = 10

    OPTIMAL_LINEUP_3B_ID = "6"
    OPTIMAL_LINEUP_3B_SALARY = 4500
    OPTIMAL_LINEUP_3B_POINTS = 14

    OPTIMAL_LINEUP_SS_ID = "7"
    OPTIMAL_LINEUP_SS_SALARY = 5600
    OPTIMAL_LINEUP_SS_POINTS = 15

    OPTIMAL_LINEUP_OF1_ID = "8"
    OPTIMAL_LINEUP_OF1_SALARY = 7200
    OPTIMAL_LINEUP_OF1_POINTS = 17

    OPTIMAL_LINEUP_OF2_ID = "9"
    OPTIMAL_LINEUP_OF2_SALARY = 6500
    OPTIMAL_LINEUP_OF2_POINTS = 15

    OPTIMAL_LINEUP_OF3_ID = "10"
    OPTIMAL_LINEUP_OF3_SALARY = 3000
    OPTIMAL_LINEUP_OF3_POINTS = 13

    OPTIMAL_LINEUP_TOTAL_SALARY = OPTIMAL_LINEUP_SP1_SALARY + OPTIMAL_LINEUP_SP2_SALARY + \
                                  OPTIMAL_LINEUP_C_SALARY + OPTIMAL_LINEUP_1B_SALARY + \
                                  OPTIMAL_LINEUP_2B_SALARY + OPTIMAL_LINEUP_3B_SALARY + \
                                  OPTIMAL_LINEUP_SS_SALARY + OPTIMAL_LINEUP_OF1_SALARY + \
                                  OPTIMAL_LINEUP_OF2_SALARY + OPTIMAL_LINEUP_OF3_SALARY

    def setUp(self):
        self.optimal_lineup = OptimalLineupDict()
        player1 = PregamePitcherGameEntry()
        player1.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_SP1_ID
        player1.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_SP1_SALARY
        player1.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_SP1_POINTS
        player1.primary_position = "SP"
        self.optimal_lineup.add(player1)

        player2 = PregamePitcherGameEntry()
        player2.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_SP2_ID
        player2.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_SP2_SALARY
        player2.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_SP2_POINTS
        player2.primary_position = "SP"
        self.optimal_lineup.add(player2)

        player3 = PregameHitterGameEntry()
        player3.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_C_ID
        player3.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_C_SALARY
        player3.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_C_POINTS
        player3.primary_position = "C"
        player3.secondary_position = "1B"
        self.optimal_lineup.add(player3)

        player4 = PregameHitterGameEntry()
        player4.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_1B_ID
        player4.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_1B_SALARY
        player4.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_1B_POINTS
        player4.primary_position = "1B"
        player4.secondary_position = "1B"
        self.optimal_lineup.add(player4)

        player5 = PregameHitterGameEntry()
        player5.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_2B_ID
        player5.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_2B_SALARY
        player5.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_2B_POINTS
        player5.primary_position = "2B"
        player5.secondary_position = "SS"
        self.optimal_lineup.add(player5)

        player6 = PregameHitterGameEntry()
        player6.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_3B_ID
        player6.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_3B_SALARY
        player6.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_3B_POINTS
        player6.primary_position = "3B"
        player6.secondary_position = "3B"
        self.optimal_lineup.add(player6)

        player7 = PregameHitterGameEntry()
        player7.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_SS_ID
        player7.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_SS_SALARY
        player7.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_SS_POINTS
        player7.primary_position = "SS"
        player7.secondary_position = "SS"
        self.optimal_lineup.add(player7)

        player8 = PregameHitterGameEntry()
        player8.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_OF1_ID
        player8.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_OF1_SALARY
        player8.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_OF1_POINTS
        player8.primary_position = "OF"
        player8.secondary_position = "OF"
        self.optimal_lineup.add(player8)

        player9 = PregameHitterGameEntry()
        player9.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_OF2_ID
        player9.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_OF2_SALARY
        player9.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_OF2_POINTS
        player9.primary_position = "OF"
        player9.secondary_position = "OF"
        self.optimal_lineup.add(player9)

        player10 = PregameHitterGameEntry()
        player10.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_OF3_ID
        player10.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_OF3_SALARY
        player10.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_OF3_POINTS
        player10.primary_position = "OF"
        player10.secondary_position = "OF"
        self.optimal_lineup.add(player10)


class TestTotalSalaryInitial(OptimalLineupTest):
    """ Test to just make sure the total salary is calculated correctly when initializing the lineup
    """

    def runTest(self):
        self.assertEqual(self.optimal_lineup.get_total_salary(), OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY)


class TestAddPlayer(OptimalLineupTest):
    """ Test of a SS where the candidate SS is a better deal than the original optimal SS
    """
    CANDIDATE_ID = "9999"
    CANDIDATE_PRIMARY_POS = "SS"
    CANDIDATE_SECONDARY_POS = "3B"
    CANDIDATE_POINTS = 10
    CANDIDATE_SALARY = 3000

    def runTest(self):
        player = PregameHitterGameEntry()
        player.rotowire_id = TestAddPlayer.CANDIDATE_ID
        player.primary_position = TestAddPlayer.CANDIDATE_PRIMARY_POS
        player.secondary_position = TestAddPlayer.CANDIDATE_SECONDARY_POS
        player.predicted_draftkings_points = TestAddPlayer.CANDIDATE_POINTS
        player.draftkings_salary = TestAddPlayer.CANDIDATE_SALARY
        self.optimal_lineup.add(player)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayer.CANDIDATE_PRIMARY_POS].get_ids()[0],
                         TestAddPlayer.CANDIDATE_ID)
        self.assertEqual(self.optimal_lineup.get_total_salary(),
                         OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY -
                         OptimalLineupTest.OPTIMAL_LINEUP_SS_SALARY +
                         TestAddPlayer.CANDIDATE_SALARY)


class TestAddPlayerWorse(OptimalLineupTest):
    """ Test of a SS where the candidate SS has a smaller points per dollar ratio than the original optimal SS
    and the original optimal 3B. Therefore, the player is not added to the lineup at either position.
    """
    CANDIDATE_ID = "9999"
    CANDIDATE_PRIMARY_POS = "SS"
    CANDIDATE_SECONDARY_POS = "3B"
    CANDIDATE_POINTS = 1
    CANDIDATE_SALARY = 4000

    def runTest(self):
        player = PregameHitterGameEntry()
        player.rotowire_id = TestAddPlayerWorse.CANDIDATE_ID
        player.primary_position = TestAddPlayerWorse.CANDIDATE_PRIMARY_POS
        player.secondary_position = TestAddPlayerWorse.CANDIDATE_SECONDARY_POS
        player.predicted_draftkings_points = TestAddPlayerWorse.CANDIDATE_POINTS
        player.draftkings_salary = TestAddPlayerWorse.CANDIDATE_SALARY
        self.optimal_lineup.add(player)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayerWorse.CANDIDATE_PRIMARY_POS].get_ids()[0],
                         OptimalLineupTest.OPTIMAL_LINEUP_SS_ID)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayerWorse.CANDIDATE_SECONDARY_POS].get_ids()[0],
                         OptimalLineupTest.OPTIMAL_LINEUP_3B_ID)

        self.assertEqual(self.optimal_lineup.get_total_salary(), OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY)


class TestAddPlayerSecondary(OptimalLineupTest):
    """ Test of a SS where the candidate SS has a smaller points per dollar ratio than the original optimal SS
    but larger then the original optimal 2B. Therefore, the player is added to the lineup at 3B.
    """
    CANDIDATE_ID = "9999"
    CANDIDATE_PRIMARY_POS = "SS"
    CANDIDATE_SECONDARY_POS = "2B"
    CANDIDATE_POINTS = (float(OptimalLineupTest.OPTIMAL_LINEUP_SS_POINTS) + OptimalLineupTest.OPTIMAL_LINEUP_2B_POINTS) / 2
    CANDIDATE_SALARY = OptimalLineupTest.OPTIMAL_LINEUP_SS_SALARY - 700

    def runTest(self):
        # Sanity check of the relationship of our parameters
        self.assertLess(TestAddPlayerSecondary.CANDIDATE_POINTS, OptimalLineupTest.OPTIMAL_LINEUP_SS_POINTS)
        self.assertGreater(TestAddPlayerSecondary.CANDIDATE_POINTS, OptimalLineupTest.OPTIMAL_LINEUP_2B_POINTS)
        self.assertLess(TestAddPlayerSecondary.CANDIDATE_SALARY / float(TestAddPlayerSecondary.CANDIDATE_POINTS),
                        OptimalLineupTest.OPTIMAL_LINEUP_2B_SALARY / float(OptimalLineupTest.OPTIMAL_LINEUP_2B_POINTS))
        self.assertLessEqual(OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY - OptimalLineupTest.OPTIMAL_LINEUP_2B_SALARY +
                             TestAddPlayerSecondary.CANDIDATE_SALARY, CONTEST_SALARY)

        player = PregameHitterGameEntry()
        player.rotowire_id = TestAddPlayerSecondary.CANDIDATE_ID
        player.primary_position = TestAddPlayerSecondary.CANDIDATE_PRIMARY_POS
        player.secondary_position = TestAddPlayerSecondary.CANDIDATE_SECONDARY_POS
        player.predicted_draftkings_points = TestAddPlayerSecondary.CANDIDATE_POINTS
        player.draftkings_salary = TestAddPlayerSecondary.CANDIDATE_SALARY
        self.optimal_lineup.add(player)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayerSecondary.CANDIDATE_PRIMARY_POS].get_ids()[0],
                         OptimalLineupTest.OPTIMAL_LINEUP_SS_ID)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayerSecondary.CANDIDATE_SECONDARY_POS].get_ids()[0],
                         TestAddPlayerSecondary.CANDIDATE_ID)

        self.assertEqual(self.optimal_lineup.get_total_salary(),
                         OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY -
                         OptimalLineupTest.OPTIMAL_LINEUP_2B_SALARY +
                         TestAddPlayerSecondary.CANDIDATE_SALARY)


class TestAddPlayerPrimary(OptimalLineupTest):
    """ Test of a 3B where the candidate 3B has a larger points per dollar ratio than the original optimal 3B
    but smaller then the original optimal SS. Therefore, the player is added to the lineup at 3B.
    """
    CANDIDATE_ID = "9999"
    CANDIDATE_PRIMARY_POS = "3B"
    CANDIDATE_SECONDARY_POS = "SS"
    CANDIDATE_POINTS = OptimalLineupTest.OPTIMAL_LINEUP_3B_POINTS
    CANDIDATE_SALARY = OptimalLineupTest.OPTIMAL_LINEUP_3B_SALARY - 100

    def runTest(self):
        player = PregameHitterGameEntry()
        player.rotowire_id = TestAddPlayerPrimary.CANDIDATE_ID
        player.primary_position = TestAddPlayerPrimary.CANDIDATE_PRIMARY_POS
        player.secondary_position = TestAddPlayerPrimary.CANDIDATE_SECONDARY_POS
        player.predicted_draftkings_points = TestAddPlayerPrimary.CANDIDATE_POINTS
        player.draftkings_salary = TestAddPlayerPrimary.CANDIDATE_SALARY
        self.optimal_lineup.add(player)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayerPrimary.CANDIDATE_PRIMARY_POS]._player.rotowire_id,
                         OptimalLineupTest.OPTIMAL_LINEUP_3B_ID)
        self.assertEqual(self.optimal_lineup.position_map[TestAddPlayerPrimary.CANDIDATE_SECONDARY_POS]._player.rotowire_id,
                         TestAddPlayerPrimary.CANDIDATE_ID)

        self.assertEqual(self.optimal_lineup.get_total_salary(),
                         OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY)
                         #TestAddPlayerPrimary.CANDIDATE_SALARY)


class TestAddOutfielder(OptimalLineupTest):
    """ Test of a 3B where the candidate 3B has a larger points per dollar ratio than the original optimal 3B
    but smaller then the original optimal SS. Therefore, the player is added to the lineup at 3B.
    """
    CANDIDATE_ID = "9999"
    CANDIDATE_PRIMARY_POS = "OF"
    CANDIDATE_SECONDARY_POS = "1B"
    CANDIDATE_POINTS = (OptimalLineupTest.OPTIMAL_LINEUP_OF1_POINTS + OptimalLineupTest.OPTIMAL_LINEUP_OF2_POINTS)/2
    CANDIDATE_SALARY = OptimalLineupTest.OPTIMAL_LINEUP_OF2_SALARY - 100

    def runTest(self):
        # Add the mediocre player
        player = PregameHitterGameEntry()
        player.rotowire_id = TestAddOutfielder.CANDIDATE_ID
        player.primary_position = TestAddOutfielder.CANDIDATE_PRIMARY_POS
        player.secondary_position = TestAddOutfielder.CANDIDATE_SECONDARY_POS
        player.predicted_draftkings_points = TestAddOutfielder.CANDIDATE_POINTS
        player.draftkings_salary = TestAddOutfielder.CANDIDATE_SALARY
        self.optimal_lineup.add(player)
        worst_player = heapq.heappop(self.optimal_lineup.position_map[TestAddOutfielder.CANDIDATE_PRIMARY_POS]._position_heap)
        self.assertEqual(self.optimal_lineup.position_map[TestAddOutfielder.CANDIDATE_PRIMARY_POS]._position_heap[0][1].rotowire_id,
                         OptimalLineupTest.OPTIMAL_LINEUP_OF1_ID)
        heapq.heappush(self.optimal_lineup.position_map[TestAddOutfielder.CANDIDATE_PRIMARY_POS]._position_heap, worst_player)
        self.assertEqual(self.optimal_lineup.position_map[TestAddOutfielder.CANDIDATE_SECONDARY_POS]._player.rotowire_id,
                         OptimalLineupTest.OPTIMAL_LINEUP_1B_ID)

        self.assertEqual(self.optimal_lineup.get_total_salary(),
                         OptimalLineupTest.OPTIMAL_LINEUP_TOTAL_SALARY -
                         OptimalLineupTest.OPTIMAL_LINEUP_1B_SALARY)


class GetSalariesTest(unittest.TestCase):
    """ Test case for testing the methods of getting the salaries for Draftkings
    """
    def test_pitcher_typical(self):
        CSV_LOCATION = "players.csv"
        NAME = "Felix Hernandez"
        TEAM = "Sea"

        csv_dict = get_csv_dict(CSV_LOCATION)
        try:
            csv_entry = csv_dict[NAME.lower() + TEAM.lower()]
        except KeyError:
            self.assertTrue(False)

        self.assertEqual(int(csv_entry["Salary"]), 10400)

    def test_hitter_typical(self):
        CSV_LOCATION = "players.csv"
        NAME = "Jon Jay"
        TEAM = "SD"

        csv_dict = get_csv_dict(CSV_LOCATION)
        try:
            csv_entry = csv_dict[NAME.lower() + TEAM.lower()]
        except KeyError:
            self.assertTrue(False)

        self.assertEqual(int(csv_entry["Salary"]), 2700)


def suite():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(GetSalariesTest)
    test_suite.addTest(TestTotalSalaryInitial())
    test_suite.addTest(TestAddPlayer())
    test_suite.addTest(TestAddPlayerWorse())
    test_suite.addTest(TestAddPlayerSecondary())
    #test_suite.addTest(TestAddPlayerPrimary())
    #test_suite.addTest(TestAddOutfielder())
    return test_suite
