import unittest

import dupi
from dupi.version import version_string


class TestVersion(unittest.TestCase):

    def test_version(self):
        self.assertTrue(dupi.__version__ >= (0, 0, 0))
        self.assertTrue(version_string() != "")
