import unittest

import baseball_reference_tdd
import draftkings_tdd
import rotowire_tdd
import lineup_tdd
import pitcher_tdd
import hitter_tdd
import stat_miner_tdd

# Baseball reference
baseball_reference_suite = baseball_reference_tdd.suite()

# Draftkings
draftkings_suite = draftkings_tdd.suite()

# Rotowire
rotowire_suite = rotowire_tdd.suite()

# Stat miner
stat_miner_suite = stat_miner_tdd.suite()

# SQL
lineup_sql_suite = lineup_tdd.suite()
pitcher_sql_suite = pitcher_tdd.suite()
hitter_sql_suite = hitter_tdd.suite()

# Run the suite
test_runner = unittest.TextTestRunner().run(unittest.TestSuite([rotowire_suite,
                                                                draftkings_suite,
                                                                baseball_reference_suite,
                                                                lineup_sql_suite,
                                                                pitcher_sql_suite,
                                                                hitter_sql_suite,
                                                                stat_miner_suite]))