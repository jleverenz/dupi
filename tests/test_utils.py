from pyfakefs import fake_filesystem_unittest

from dupi import utils


class TestUtils(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_walk_dir_excludes_visitied_dirs(self):
        self.fs.CreateFile('/test/file1', contents='abc')
        self.fs.CreateFile('/test/sub/file2', contents='abc')

        filelist = utils.generate_filelist(['/test/sub', '/test'])
        self.assertEqual(2, len(filelist))
