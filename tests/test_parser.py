import unittest
from formata import parser


class DataNetCDFTestCase(unittest.TestCase):

    def test_ds_dir_unavailable(self):
        wrong_dir = 'D:/ddrive/agmerra_net_filesa'
        data = parser.DataNetCDF(wrong_dir)
        self.assertIsNone(data.get_datasets(wrong_dir), "Result should be None when directory doesn't exist")

    def test_no_nc_found(self):
        wrong_dir = 'D:/ddrive/'
        data = parser.DataNetCDF(wrong_dir)
        self.assertIsNone(data.get_datasets(wrong_dir), "Result should be None when no .nc files found")


if __name__ == '__main__':
    unittest.main()
