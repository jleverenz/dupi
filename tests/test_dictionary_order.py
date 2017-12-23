from tests.common import *      # dupi/tests/common

import io
import random

from pyfakefs import fake_filesystem_unittest

from dupi import conf, core
from dupi.index import Index

from unittest.mock import patch


class ShufflingDict(dict):
    def keys(self):
        k = list(super().keys())
        random.shuffle(k)
        return k

    def values(self):
        v = list(super().values())
        random.shuffle(v)
        return v

    def items(self):
        items = list(super().items())
        random.shuffle(items)
        return items


# @patch requires create=True for py versions < 3.5. It is optional in 3.5+.
@patch('dupi.index.dict', wraps=ShufflingDict, create=True)
class TestDictionaryOrder(fake_filesystem_unittest.TestCase):

    # Override run() to wrap each test in a context redirecting stderr
    def run(self, result=None):
        err_out = io.StringIO()
        with redirect_stderr(err_out):
            super().run(result)

    def setUp(self):
        self.setUpPyfakefs()

        # Touch the default index file location on fake filesystem,
        # to be sure parent dir structure exists.
        self.fs.CreateFile(conf.index_file, create_missing_dirs=True)

        # Setup index
        self.index = Index(conf.index_file)

    def test_list(self, dict_mock):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        self.fs.CreateFile('/test/file3', contents='abc')

        core.update_index(self.index, ['/test'])
        results = core.list_duplicates(self.index)
        self.assertSetEqual(set(results), {'/test/file2', '/test/file3'})
