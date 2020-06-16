import formata.parser as parser
import formata.utils as utils
from pathlib import Path
import glob


class NCToWTHConverter:
    """
    A Converter class to WTH files from global NetCDF weather data
    """

    def __init__(self, src_dir):
        self.src_dir = src_dir

    def check_dir(self):

        if not Path(self.src_dir).exists():
            print('No such directory found:', self.src_dir)
            return

        nc_all = self.src_dir + "/*.nc*"
        if len(glob.glob(nc_all)) == 0:
            print('No NetCDF files found in:', self.src_dir)
            return

        return nc_all

    def is_out_dir_present(self, dest_dir):
        if not Path(dest_dir).exists():
            print('No such output directory found:', dest_dir)
            return False
        return True

    def toWTH(self, dest_dir):

        if not self.is_out_dir_present(dest_dir):
            return

        nc_dir = self.check_dir()
        if nc_dir is None:
            return