"""
parses string in  rfc 3339 format
input:
    datetime_str_full - string containing datetime in rfc 3339
output:
    rtc - RTC object that has been set with current time
"""
def parse_datetime_string(datetime_str_full):
    from machine import RTC

    # 2017-01-16 02:09:20+00:00
    # parse datetime string
    datetime_str, subsec_str = str(datetime_str_full).split('+')
    date_str, time_str = datetime_str.split(' ')
    year_str, mon_str, day_str = date_str.split('-')
    hour_str, min_str, sec_str = time_str.split(':')
    datetime_tuple = (int(year_str), int(mon_str), int(day_str), int(0), int(hour_str), int(min_str), int(sec_str), int(0))

    rtc = RTC() # set up clock object
    rtc.datetime(datetime_tuple) # set initial time

    return rtc

"""
returns current time as string in  rfc 3339 format
input:
    datetime_str_full - string containing datetime in rfc 3339
output:
    rtc - RTC object that has been set with current time
"""
def get_time_string(rtc):
    from machine import RTC

    dt_t = rtc.datetime() # short for datetime_tuple
    datetime_str = str(dt_t[0]) + '-' + str(dt_t[1]) + '-' + str(dt_t[2]) + ' ' + str(dt_t[4]) + ':' + str(dt_t[5]) + ':' + str(dt_t[6]) + '+00:00'
    return datetime_str
