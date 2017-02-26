import io
import sys

from pyfakefs import fake_filesystem_unittest

from dupi import conf, core
from dupi.storage import Storage


# TODO order is not deterministic while based on os.walk
class TestReporting(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        # Touch the default index file location on fake filesystem,
        # to be sure parent dir structure exists.
        self.fs.CreateFile(conf.index_file, create_missing_dirs=True)

        # Setup index
        self.index = Storage(conf.index_file)

    def test_list_empty(self):
        core.update_index(self.index, ['/test'])
        results = core.list_duplicates(self.index)
        self.assertEqual(0, len(list(results)))

    def test_list_no_duplicates(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file3', contents='defg')
        self.fs.CreateFile('/test/file4', contents='hijk')

        core.update_index(self.index, ['/test'])
        results = core.list_duplicates(self.index)
        self.assertEqual(0, len(list(results)))

    def test_list(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        self.fs.CreateFile('/test/file3', contents='defg')
        self.fs.CreateFile('/test/file4', contents='hijk')
        self.fs.CreateFile('/test/afile', contents='abc')

        core.update_index(self.index, ['/test'])
        results = core.list_duplicates(self.index)
        self.assertSetEqual(set(results), {'/test/file1', '/test/file2'})

    def test_list_with_originals(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        self.fs.CreateFile('/test/file3', contents='defg')
        self.fs.CreateFile('/test/file4', contents='hijk')
        self.fs.CreateFile('/test/afile', contents='abc')

        core.update_index(self.index, ['/test'])
        results = core.list_duplicates_with_originals(self.index)
        self.assertEqual(1, len(results))
        orig, *dupes = results[0]
        self.assertEqual('/test/afile', orig)
        self.assertSetEqual(set(dupes),
                            {'/test/file1', '/test/file2'})

    def test_list_empty_with_originals(self):
        core.update_index(self.index, ['/test'])
        results = core.list_duplicates_with_originals(self.index)
        self.assertEqual(0, len(results))

    def test_list_no_duplicates_with_originals(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file3', contents='defg')
        self.fs.CreateFile('/test/file4', contents='hijk')

        core.update_index(self.index, ['/test'])
        results = core.list_duplicates_with_originals(self.index)
        self.assertEqual(0, len(results))

    def test_list_duplicates_with_originals_pairs(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')

        core.update_index(self.index, ['/test'])
        results = core.list_duplicates_with_originals(self.index)
        self.assertEqual(1, len(results))
        self.assertSetEqual(set(results[0]), {'/test/file1', '/test/file2'})
