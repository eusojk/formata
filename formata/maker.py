import formata.parser as parser
import formata.utils as ut
from pathlib import Path
import os
import shutil
import glob


class NCToWTHConverter:
    """
    A Converter class to WTH files from global NetCDF weather data
    """

    def __init__(self, src_dir, country="globe"):
        self.src_dir = src_dir
        self.years = ut.make_wth_dates_format()
        self.country = self.check_country(country)

    def check_dir(self):
        """
        Checks if the .NC files/dir exists
        :return: path to the directory
        """
        if not Path(self.src_dir).exists():
            print('No such directory found:', self.src_dir)
            return

        nc_all = self.src_dir + "/*.nc*"
        if len(glob.glob(nc_all)) == 0:
            print('No NetCDF files found in:', self.src_dir)
            return

        return nc_all

    def check_country(self, country):

        if country == "globe":
            return country

        iso = ut.get_country_iso(country)
        if iso is None:
            return
        else:
            return country

    # noinspection PyMethodMayBeStatic
    def is_out_dir_present(self, dest_dir):
        """
        Check if the output dir given exists on disk
        :param dest_dir: path - where to save .WTH
        :return: bool
        """
        if not Path(dest_dir).exists():
            print('No such output directory found:', dest_dir)
            return False
        return True

    def print_country_boundary(self, data):
        """

        :return:
        """
        print( data.get_country_boundary("England"))

    def to_WTH(self, dest_dir):
        """
        caller function to to_WTH_converter
        :param dest_dir: path - where to save .WTH
        :return:
        """
        if not self.is_out_dir_present(dest_dir):
            return

        nc_dir = self.check_dir()
        if nc_dir is None:
            return

        weather_data = parser.WeatherDataNC(nc_dir)
        self.to_WTH_converter(weather_data, dest_dir)


    def to_WTH_converter(self, weather_data, dest_dir):
        """
        Main function responsible for conversion
        :param weather_data: xarray dataset containing global weather data
        :param dest_dir: path to  export .WTH
        :return:
        """
        ds_all = weather_data.get_global_dataset()
        if self.country is None:
            print("Country given is erroneous:")
            return
        elif self.country == "globe":
            lon_num_start = 0
            lon_num_stop  = weather_data.get_num_of_attribute('longitude')
            lat_num_start = 0
            lat_num_stop  = weather_data.get_num_of_attribute('latitude')
        else:
            lon_num_start, lon_num_stop, lat_num_start, lat_num_stop = weather_data.get_country_boundary(self.country)


        # top bottom, left to right
        for lon_i in range(lon_num_start, lon_num_stop + 1):
        # for lon_i in range(lon_num_start, lon_num_stop+1):
            lon = ds_all.longitude.isel(longitude=lon_i).values.tolist()

            for lat_i in range(lat_num_start, lat_num_stop+1):
            # for lat_i in range(lat_num_start, lat_num_stop + 1):
                lat = ds_all.latitude.isel(latitude=lat_i).values.tolist()

                # create a dynamic header with updated LON, LAT info and move it into the folder given
                wth_header_u = ut.format_header(lat_i + 1, lon_i + 1, lat, lon)
                wth_header = dest_dir + "/" + wth_header_u
                shutil.move(wth_header_u, wth_header)

                # open in appending mode
                fwth = open(wth_header, "a+")

                # loop through daily weather data
                for t, date in enumerate(self.years):
                    daily_data_vars = ut.get_daily_data_vars(ds_all, lat_i, lon_i, t)
                    # disregard all NAN values
                    if daily_data_vars is None:
                        fwth.close()
                        os.remove(wth_header)
                        break

                    if t == 0:
                        ut.update_table(wth_header_u, lat, lon)

                    entry = ut.format_data_vars_entry(daily_data_vars, date)

                    # append this entry into the file
                    fwth.write(entry)
                    print("Added entry:", entry)

                # close file after writing
                fwth.close()
                print("Output WTH:", wth_header)
