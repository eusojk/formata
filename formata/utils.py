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


def make_wth_dates_format():
    """
    Format to WTH Date: e.g. 1st of 1980 => 80001
    :return: a list of string dates
    """
    all_years = [1980 + x for x in range(31)]
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

    :param ds_all:
    :param lat:
    :param lon:
    :param timeval:
    :return:
    """
    data_vars_dict = collections.OrderedDict()
    ds = ds_all.isel(time=timeval, latitude=lat, longitude=lon)
    srad = ds.srad.values.tolist()

    # watch out for NaN values
    if (math.isnan(srad)):
        return

    data_vars_dict['SRAD'] = round(srad, 1)
    data_vars_dict['TMAX'] = round(ds.tmax.values.tolist(), 1)
    data_vars_dict['TMIN'] = round(ds.tmin.values.tolist(), 1)
    data_vars_dict['RAIN'] = round(ds.prate.values.tolist(), 1)
    data_vars_dict['WIND'] = round(ds.wndspd.values.tolist(), 1)
    data_vars_dict['RHUM'] = round(ds.rhstmax.values.tolist(), 1)
    data_vars_dict['TAVG'] = round(ds.tavg.values.tolist(), 1)

    return data_vars_dict