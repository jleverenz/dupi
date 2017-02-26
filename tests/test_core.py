from pyfakefs import fake_filesystem_unittest
from dupi import conf, core
from dupi.storage import Storage


class TestCore(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        # Touch the default index file location on fake filesystem,
        # to be sure parent dir structure exists.
        self.fs.CreateFile(conf.index_file, create_missing_dirs=True)

        # Setup index
        self.index = Storage(conf.index_file)

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

    def test_update_index_deletes_removed_files(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/file2', contents='def')

        core.update_index(self.index, ['/test'])

        self.fs.RemoveObject('/test/file2')

        core.update_index(self.index, ['/test'])

        self.assertEqual(1, len(self.index.all()))
