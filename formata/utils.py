import math
import os
import collections

PAD = 6
PAD_LON_LAT = 9
TITLE_W = '*WEATHER DATA : '
EXT_NC = '.agmerra.nc\n'
HEADER_L1 = '@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT\n'
HEADER_L2 = '    CI   49.250  -99.750   -99   3.5  34.7   -99    10\n'
HEADER_L3 = '@DATE  SRAD  TMAX  TMIN  RAIN  WIND  RHUM  TAVG\n'

TABLEDB = os.path.dirname(os.path.realpath(__file__)) + "/templates/table.txt"

def is_leap_year(year):
    """
    Check if a given year is leap
    :param year: 4-digit year
    :return: True or False
    """
    check = ((year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)))
    return True if check else False


def format_data_vars_entry(data_vars, date, padding=6):
    """
    Transforms weather data info into formatted daily entry:
        e.g. 82058  11.0  -9.5 -22.6   0.0 334.8
    :param data_vars: an ordered Dict containing 7 weather variables data
    :param date: a string representing a date. e.g 82058
    :param padding: # of space before value
    :return: formatted string
    """
    entry = ''
    for k, v in data_vars.items():
        v_str = str(v)
        v_str = v_str.rjust(padding)
        entry += v_str

    entry = date + entry + '\n'
    return entry


def make_wth_dates_format(start_year=1980, num_year=30):
    """
    Format to WTH Date: e.g. 1st of 1980 => 80001
    :param start_year: starting year of data (usually, for forecasting, 1980)
    :param num_year: number of years after initial year (usually, for forecasting, 30)
    :return: list of date in WTH format
    """
    all_years = [start_year + x for x in range(num_year + 1)]
    years_formated = []

    for yr in all_years:
        if is_leap_year(yr):
            ndays = 366
        else:
            ndays = 365

        for d in range(1, ndays + 1):
            # if year is 1980 and day is 1: 80 + 001 => 80001
            yr_str = str(yr)[-2:] + str(d).rjust(3, '0')
            years_formated.append(yr_str)

    return years_formated


def get_daily_data_vars(ds_all, lat, lon, timeval):
    """
    This function retrieves weather variables at a location
    :param ds_all: an xarray dataset containing global weather data from 1980 - 2010
    :param lat: latitude
    :param lon: longitude
    :param timeval: time (# of days)
    :return: an ordered dictionary
    """
    data_vars_dict = collections.OrderedDict()
    ds = ds_all.isel(time=timeval, latitude=lat, longitude=lon)
    srad = ds.srad.values.tolist()
    tmax = ds.tmax.values.tolist()
    tmin = ds.tmin.values.tolist()
    prate = ds.prate.values.tolist()
    wndspd = ds.wndspd.values.tolist()
    rhstmax = ds.rhstmax.values.tolist()
    tavg = ds.tavg.values.tolist()

    # watch out for NaN values
    all_nan = math.isnan(srad) and math.isnan(tmax) and math.isnan(tmin) and math.isnan(prate) \
              and math.isnan(wndspd) and math.isnan(rhstmax) and math.isnan(tavg)
    if all_nan:
        return

    if math.isnan(srad):
        srad = -99
    if math.isnan(tmax):
        tmax = -99
    if math.isnan(tmin):
        tmin = -99
    if math.isnan(prate):
        prate = -99
    if math.isnan(wndspd):
        wndspd = -99
    if math.isnan(rhstmax):
        rhstmax = -99
    if math.isnan(tavg):
        tavg = -99

    data_vars_dict['SRAD'] = round(srad, 1)
    data_vars_dict['TMAX'] = round(tmax, 1)
    data_vars_dict['TMIN'] = round(tmin, 1)
    data_vars_dict['RAIN'] = round(prate, 1)
    data_vars_dict['WIND'] = round(wndspd, 1)
    data_vars_dict['RHUM'] = round(rhstmax, 1)
    data_vars_dict['TAVG'] = round(tavg, 1)

    return data_vars_dict


def format_header(lat_i, lon_i, lat, lon, pad_lat=3, pad_lon=4):
    """
    Responsible for formatting the header of .WTH files
    :param lat_i: index position of given latitude value in the dataset
    :param lon_i: index position of given longitude value in the dataset
    :param lat: float - latitude value
    :param lon: float - longitude value
    :param pad_lat: int - justify lat value (3)
    :param pad_lon: int - justify lon value (4)
    :return: file/path
    """
    base = str(lat_i).rjust(pad_lat, '0') + "_" + str(lon_i).rjust(pad_lon, '0')
    wth_name = base + ".WTH"
    name_index = str(lat).rjust(PAD_LON_LAT) + str(lon).rjust(PAD_LON_LAT)

    header_line1 = TITLE_W + base + EXT_NC
    header_line2 = 'CI'.rjust(PAD) + name_index + 5 * ('-99'.rjust(PAD)) + '\n'

    fwth = open(wth_name, "w+")
    fwth.write(header_line1)
    fwth.write(HEADER_L1)
    fwth.write(header_line2)
    fwth.write(HEADER_L3)
    fwth.close()

    return wth_name

def update_table(wth_file, lat, lon):
    """
    Append this entry to table.txt
    :return:
    """
    name_index = str(lat).rjust(PAD_LON_LAT) + str(lon).rjust(PAD_LON_LAT)
    entry = wth_file + name_index + '\n'

    with open(TABLEDB, "a") as f:
        f.write(entry)
        f.close()