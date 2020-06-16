import numpy as np
import xarray as xr


class DataNetCDF:
    """

    """

    def __init__(self, nc_dir):

        self.nc_dir = nc_dir
        self.ds_all = xr.open_mfdataset(self.nc_dir, decode_times=False, combine='by_coords', engine='netcdf4',
                                        parallel=True)
        self.ds_dims = dict(self.ds_all.dims)

    def get_num_of_attribute(self, attr):
        if attr in self.ds_dims.keys():
            return self.ds_dims[attr]
        return
