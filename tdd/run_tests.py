import unittest

import baseball_reference_tdd
import draftkings_tdd
import rotowire_tdd
import lineup_tdd

# Baseball reference
baseball_reference_suite = baseball_reference_tdd.suite()

# Draftkings
draftkings_suite = draftkings_tdd.suite()

# Rotowire
rotowire_suite = rotowire_tdd.suite()

# SQL
sql_suite = lineup_tdd.suite()

# Run the suite
test_runner = unittest.TextTestRunner().run(unittest.TestSuite([draftkings_suite,
                                                                baseball_reference_suite,
                                                                rotowire_suite,
                                                                sql_suite]))