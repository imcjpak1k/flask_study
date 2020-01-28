import datetime

# https://docs.python.org/ko/3/library/datetime.html

def current_datetime():
    return datetime.datetime.now()

def current_datetime_fmt(fmt="%Y%m%d%H%M%S%f"):
    return current_datetime().strftime(fmt)

def current_date():
    return datetime.date.today()

def current_date_fmt(fmt="%Y%m%d"):
    return current_date().strftime(fmt)

def date_strfmt(date, fmt="%Y%m%d"):
    '''
    date객체를 포맷(fmt)형태의 문자열로 반환
    '''
    return date.strftime(fmt)

def datetime_strfmt(datetime, fmt="%Y%m%d%H%M%S%f"):
    '''
    datetime객체를 포맷(fmt)형태의 문자열로 반환
    '''
    return datetime.strftime(fmt)

def strfmt_date(yyyymmdd):
    '''
    문자열의 날자(YYYYMMDD)를 date객체로 반환
    '''
    return datetime.date(
        int(yyyymmdd[0:4]), 
        int(yyyymmdd[4:6]), 
        int(yyyymmdd[6:]),
    )