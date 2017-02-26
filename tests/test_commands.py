import io
import re
import sys

from pyfakefs import fake_filesystem_unittest

from dupi import conf, core
from dupi.commands import dispatch
from dupi.storage import Storage


class TestCommands(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        # Touch the default index file location on fake filesystem,
        # to be sure parent dir structure exists.
        self.fs.CreateFile(conf.index_file, create_missing_dirs=True)

    def test_update_command(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')

        index = Storage(conf.index_file)

        params = {'dirs': ['/test']}
        dispatch(index, 'update', **params)

        self.fs.RemoveObject('/test/file2')
        dispatch(index, 'update')

        self.assertEqual(1, len(index.all()))

    def test_report_command(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        self.fs.CreateFile('/test/file3', contents='defg')
        self.fs.CreateFile('/test/file4', contents='hijk')
        self.fs.CreateFile('/test/afile', contents='abc')

        _old_stdout = sys.stdout
        stdout_cap = io.StringIO()
        sys.stdout = stdout_cap

        index = Storage(conf.index_file)
        core.update_index(index, ['/test'])
        dispatch(index, 'report')

        sys.stdout = _old_stdout

        # Just check that three lines got written..
        self.assertEqual(3, len(stdout_cap.getvalue().strip().split("\n")))

    def test_report_stats(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='abc')
        self.fs.CreateFile('/test/file3', contents='defg')
        self.fs.CreateFile('/test/file4', contents='hijk')
        self.fs.CreateFile('/test/afile', contents='abc')

        _old_stdout = sys.stdout
        stdout_cap = io.StringIO()
        sys.stdout = stdout_cap

        index = Storage(conf.index_file)
        core.update_index(index, ['/test'])
        dispatch(index, 'stats')

        sys.stdout = _old_stdout

        self.assertRegex(stdout_cap.getvalue(),
                         re.compile('file records', re.M))
