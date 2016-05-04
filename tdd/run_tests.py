import unittest

import baseball_reference_tdd
import draftkings_tdd

# Baseball reference
test_suite = baseball_reference_tdd.suite()
test_runner = unittest.TextTestRunner().run(test_suite)

# Draftkings
test_suite = draftkings_tdd.suite()
test_runner = unittest.TextTestRunner().run(test_suite)