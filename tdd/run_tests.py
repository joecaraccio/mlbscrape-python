import unittest

import baseball_reference_tdd

test_suite = baseball_reference_tdd.suite()
test_runner = unittest.TextTestRunner().run(test_suite)