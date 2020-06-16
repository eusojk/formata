import glob
import numpy as np
import xarray as xr
from pathlib import Path


class NCToWTHConverter:
    """
    A Converter class to WTH files from gloabl NetCDF weather data
    """

    def __init__(self, nc_dir):

        self.nc_dir = self.get_datasets(nc_dir)
        if self.nc_dir is not None:
            self.ds_all = self.merge_datasets()
            self.ds_dims = dict(self.ds_all.dims)

    def merge_datasets(self):
        ds_all = xr.open_mfdataset(self.nc_dir, decode_times=False, combine='by_coords', engine='netcdf4',
                                   parallel=True)
        return ds_all

    def get_num_of_attribute(self, attr):
        if attr in self.ds_dims.keys():
            return self.ds_dims[attr]
        return

    def get_global_dataset(self):
        return self.ds_all

    def get_datasets(self, nc_dir):

        if not Path(nc_dir).exists():
            print('No such directory found:', nc_dir)
            return

        nc_all = nc_dir + "/*.nc*"
        if len(glob.glob(nc_all)) == 0:
            print('No NetCDF files found in:', nc_dir)
            return

        return nc_all
