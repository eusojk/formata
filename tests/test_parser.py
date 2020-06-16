import unittest
from formata import parser
from formata import maker

class NCToWTHConverterTestCase(unittest.TestCase):

    def test_ds_dir_unavailable(self):
        inp = 'D:/ddrive/agmerra_net_filesa'
        data = maker.NCToWTHConverter(inp)
        self.assertIsNone(data.check_dir(), "no nc files present")


if __name__ == '__main__':
    unittest.main()
