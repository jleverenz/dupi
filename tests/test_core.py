from tests.common import *      # dupi/tests/common

import io

from pyfakefs import fake_filesystem, fake_filesystem_unittest

from dupi import conf, core
from dupi.index import Index

from unittest.mock import patch


class TestCore(fake_filesystem_unittest.TestCase):

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

    def test_update_index_with_single_file(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        core.update_index(self.index, ['/test'])

        self.assertEqual(len(self.index.all()), 1)

    def test_update_index_without_change(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='def')
        core.update_index(self.index, ['/test'])

        orig = dict()
        for i in self.index.all():
            orig[i['fullpath']] = i

        core.update_index(self.index, ['/test'])

        for i in self.index.all():
            self.assertEqual(i, orig[i['fullpath']])

    def test_update_index_on_content_change(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='def')

        core.update_index(self.index, ['/test'])

        shas = dict()
        for i in self.index.all():
            shas[i['fullpath']] = i['sha256']

        with open('/test/file2', "w") as f:
            f.write('ghi')

        core.update_index(self.index, ['/test'])

        file1_sha = self.index.get('/test/file1')['sha256']
        file2_sha = self.index.get('/test/file2')['sha256']

        self.assertEqual(shas['/test/file1'], file1_sha)
        self.assertNotEqual(shas['/test/file2'], file2_sha)

    def test_update_index_deletes_and_updates_files(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='def')

        core.update_index(self.index, ['/test'])
        sha = self.index.get('/test/file1')['sha256']

        with open('/test/file1', "w") as f:
            f.write('ghi')
        self.fs.RemoveObject('/test/file2')

        core.update_index(self.index)

        self.assertEqual(1, len(self.index.all()))
        self.assertNotEqual(sha, self.index.get('/test/file1')['sha256'])

    def _delete_file_before_stat(self, f):
        # This function is used in tests below to simulate a file being deleted
        # while dupi is processing. Since dupi will build file lists first, and
        # then process them, there's a window where a file my be removed and is
        # no longer processable. This simulates that behavior by destroying
        # files immediately before os.stat is called.

        fake_os = fake_filesystem.FakeOsModule(self.fs)
        # delete the file right before calling
        self.fs.RemoveObject(f)
        return fake_os.stat(f)

    def test_update_with_dirs_handles_disappearing_files(self):
        self.fs.CreateFile('/test/blahfile', contents='abc')

        with patch('dupi.index.os.path',
                   side_effect=self._delete_file_before_stat):
            core.update_index(self.index, ['/test'])

        # Nothing added .. the file disappeared
        self.assertEqual(len(self.index.all()), 0)

    def test_update_empty_handles_disappearing_files(self):
        self.fs.CreateFile('/test/blahfile', contents='abc')

        core.update_index(self.index, ['/test'])
        self.assertEqual(len(self.index.all()), 1)

        with patch('dupi.index.os.stat',
                   side_effect=self._delete_file_before_stat):
            core.update_index(self.index, [])

        self.assertEqual(len(self.index.all()), 0)

    def test_update_index_deletes_removed_files(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='def')

        core.update_index(self.index, ['/test'])

        self.fs.RemoveObject('/test/file2')

        core.update_index(self.index, ['/test'])

        self.assertEqual(1, len(self.index.all()))
