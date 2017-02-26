import io
import sys

from pyfakefs import fake_filesystem_unittest

from dupi import conf
from dupi.__main__ import main
from dupi.storage import Storage
import dupi.commands


class TestMain(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        # Touch the default index file location on fake filesystem,
        # to be sure parent dir structure exists.
        self.fs.CreateFile(conf.index_file, create_missing_dirs=True)

    def test_update(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')

        main(['update', '/test'])

        index = Storage(conf.index_file)
        self.assertEqual(len(index.all()), 2)

    def test_update_empty(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')

        main(['update', '/test'])
        index = Storage(conf.index_file)
        sha = index.get('/test/file1')['sha256']
        with open('/test/file1', "w") as f:
            f.write('ghi')
        self.fs.RemoveObject('/test/file2')
        main(['update'])

        index = Storage(conf.index_file)
        self.assertEqual(1, len(index.all()))
        self.assertNotEqual(sha, index.get('/test/file1')['sha256'])

    def test_update_and_purge(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        main(['update', '/test'])

        index = Storage(conf.index_file)
        self.assertEqual(len(index.all()), 2)

        main(['purge'])
        index = Storage(conf.index_file)
        self.assertEqual(0, len(index.all()))

    def test_update_and_list(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')

        _old_stdout = sys.stdout
        stdout_cap = io.StringIO()
        sys.stdout = stdout_cap

        main(['update', '/test'])
        main(['list'])
        sys.stdout = _old_stdout
