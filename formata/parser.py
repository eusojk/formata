import glob
import numpy as np
import xarray as xr
from pathlib import Path


class WeatherDataNC:
    """
    A representation of global NetCDF weather data
    """

    def __init__(self, nc_dir):

        self.nc_dir = nc_dir
        self.ds_all = self.merge_datasets()
        self.ds_dims = dict(self.ds_all.dims)

    def merge_datasets(self):
        ds_all = xr.open_mfdataset(self.nc_dir, decode_times=False, combine='by_coords', engine='netcdf4')
        return ds_all

    def get_num_of_attribute(self, attr):
        if attr in self.ds_dims.keys():
            return self.ds_dims[attr]
        return

    def get_global_dataset(self):
        return self.ds_all

