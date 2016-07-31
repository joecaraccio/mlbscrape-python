import unittest

import baseball_reference_tdd
import draftkings_tdd

# Baseball reference
#baseball_reference_suite = baseball_reference_tdd.suite()

# Draftkings
draftkings_suite = draftkings_tdd.suite()

# Run the suite
test_runner = unittest.TextTestRunner().run(unittest.TestSuite([draftkings_suite]))