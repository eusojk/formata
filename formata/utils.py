import math
import collections


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

    entry = date + entry
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

    # watch out for NaN values
    if math.isnan(srad):
        return

    data_vars_dict['SRAD'] = round(srad, 1)
    data_vars_dict['TMAX'] = round(ds.tmax.values.tolist(), 1)
    data_vars_dict['TMIN'] = round(ds.tmin.values.tolist(), 1)
    data_vars_dict['RAIN'] = round(ds.prate.values.tolist(), 1)
    data_vars_dict['WIND'] = round(ds.wndspd.values.tolist(), 1)
    data_vars_dict['RHUM'] = round(ds.rhstmax.values.tolist(), 1)
    data_vars_dict['TAVG'] = round(ds.tavg.values.tolist(), 1)

    return data_vars_dict
