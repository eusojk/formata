import xarray as xr
from formata import utils

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

    def get_country_boundary(self, country):
        try:
            # min_lon, min_lat, max_lon, max_lat = utils.get_country_bbox(country)
            # min_lon, min_lat, max_lon, max_lat = -104.05, 45.94, -96.55, 49.0 # North Dakota -done
            # min_lon, min_lat, max_lon, max_lat = -108.619, 46.57198, -94.5712, 54.25233   # CA WEST - running
            # min_lon, min_lat, max_lon, max_lat = -84.5933, 40.30297, -62.8651, 51.13424       # CA EAST - next
            # min_lon, min_lat, max_lon, max_lat = -14.02,49.67,2.09,61.06   # UK - next

            # min_lon, min_lat, max_lon, max_lat = -4.492328, 50.61108, 0.6076721, 57.51106   # UK - Missing - running
            min_lon, min_lat, max_lon, max_lat = -83.09328, 41.80296, -64.19308, 50.20294   # CE - Missing
            # min_lon, min_lat, max_lon, max_lat = -108.319, 47.47197, -95.41888, 54.07196    # CW - Missing
        except:
            print("Error unpacking boundingbox")
            return
        min_lon = int(min_lon) + 0.875
        max_lon = int(max_lon) + 0.125
        min_lat = int(min_lat) + 0.125
        max_lat = int(max_lat) + 0.875

        min_lon_index = self.ds_all.longitude.values.tolist().index(min_lon)
        max_lon_index = self.ds_all.longitude.values.tolist().index(max_lon)
        # Lat values go from positive (top) to negative (bottom)
        min_lat_index = self.ds_all.latitude.values.tolist().index(max_lat)
        max_lat_index = self.ds_all.latitude.values.tolist().index(min_lat)

        # country_lon_list = self.ds_all.longitude.values.tolist()[min_lon_index:max_lon_index + 1]
        # country_lat_list = self.ds_all.latitude.values.tolist()[min_lat_index:max_lat_index + 1]
        boundary = (min_lon_index, max_lon_index, min_lat_index, max_lat_index)
        return boundary