import unittest

from formata import maker


class NCToWTHConverterTestCase(unittest.TestCase):

    def test_ds_dir_unavailable(self):
        inp = 'D:/ddrive/agmerra_net_filesa'
        data = maker.NCToWTHConverter(inp)
        self.assertIsNone(data.check_dir(), "no nc files present")

    def test_nc_files_present(self):
        inp = 'D:/ddrive/agmerra_net_files'
        data = maker.NCToWTHConverter(inp)
        self.assertIsNotNone(data.check_dir(), "nc files present")


if __name__ == '__main__':
    unittest.main()
