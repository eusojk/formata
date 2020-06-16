import formata.parser as parser
import formata.utils as ut
from pathlib import Path
import glob


class NCToWTHConverter:
    """
    A Converter class to WTH files from global NetCDF weather data
    """

    def __init__(self, src_dir):
        self.src_dir = src_dir
        self.years = ut.make_wth_dates_format()

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

    def to_WTH(self, dest_dir):

        if not self.is_out_dir_present(dest_dir):
            return

        nc_dir = self.check_dir()
        if nc_dir is None:
            return

    def to_WTH_converter(self, weather_data):
        ds_all = weather_data.get_global_dataset
        lon_num = weather_data.get_num_of_attribute('longitude')
        lat_num = weather_data.get_num_of_attribute('latitude')

        # top bottom, left to right
        for lon_i in range(lon_num):
            lon = ds_all.longitude.isel(longitude=lon_i).values.tolist()

            for lat_i in range(lat_num):
                lat = ds_all.latitude.isel(latitude=lat_i).values.tolist()

                # call format_header(lon, lat) here

                for t, date in enumerate(self.years):
                    daily_data_vars = ut.get_daily_data_vars(ds_all, lat_i, lon_i, t)
                    # disregard all NAN values
                    if daily_data_vars is None:
                        break

                    entry = ut.format_data_vars_entry(daily_data_vars, date)

                    # call a function to write each entry to a file
