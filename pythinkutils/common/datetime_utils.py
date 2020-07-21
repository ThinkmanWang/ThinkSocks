# -*- coding: utf-8 -*-

import time
from datetime import date, timedelta
import datetime

def get_timestamp():
    return int(time.time())

def get_current_time_str():
    temp = time.localtime(time.time())
    szTime = time.strftime("%Y-%m-%d %H:%M:%S", temp)
    return szTime

def timestamp2str(tt):
    t1 = time.localtime(float(tt))
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t1)
    return t2

def timestamp2date(tt):
    t1 = time.localtime(float(tt))
    t2 = time.strftime("%Y-%m-%d", t1)
    return t2

def hour():
    temp = time.localtime(time.time())
    szTime = time.strftime("%H", temp)
    return int(szTime)

def today():
    today = date.today()
    return today.strftime('%Y-%m-%d')

def yesterday():
    yesterday = date.today() + timedelta(-1)
    return yesterday.strftime('%Y-%m-%d')

def diff_day(nDiff):
    day = date.today() + timedelta(nDiff)
    return day.strftime('%Y-%m-%d')

def addmonths(date,months = 0):
    targetmonth=months+date.month
    try:
        if 0 == targetmonth%12:
            return date.replace(year=date.year+int(targetmonth/12) - 1,month=12)
        else:
            return date.replace(year=date.year + int(targetmonth / 12), month=(targetmonth % 12))
    except Exception as e:
        # There is an exception if the day of the month we're in does not exist in the target month
        # Go to the FIRST of the month AFTER, then go back one day.
        date.replace(year=date.year+int((targetmonth+1)/12),month=((targetmonth+1)%12),day=1)
        date+=datetime.timedelta(days=-1)
        return date

def last_day_of_month_by_date(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def first_day_of_month(nDiffMon = 0):
    today = date.today()
    date1 = addmonths(today.replace(day=1), nDiffMon)
    return date1.replace(day=1)

def last_day_of_month(nDiffMon = 0):
    def end_day(any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)

    return end_day(first_day_of_month(nDiffMon))

def date_between_start_end(szStart, szEnd):
    dateStart = datetime.datetime.strptime(szStart, '%Y-%m-%d')
    dateEnd = datetime.datetime.strptime(szEnd, '%Y-%m-%d')

    lstDate = []
    lstDate.append(szStart)

    while dateStart < dateEnd:
        dateStart += datetime.timedelta(days=1)
        lstDate.append(dateStart.strftime('%Y-%m-%d'))

    return lstDate

def start_end_of_week(nYear, nWeek):
    dateStart = time.strptime('{}-{}-1'.format(str(nYear).zfill(4), str(nWeek).zfill(2)), '%Y-%U-%w')
    dateStart = time.mktime(dateStart)

    dateEnd = int(dateStart) + 3600 * 24 * 6

    return timestamp2date(dateStart), timestamp2date(dateEnd)

# print(date_between_start_end("2019-03-02", "2019-03-03"))
# print(date_between_start_end("2019-03-02", "2019-03-02"))
# print(date_between_start_end("2019-03-03", "2019-03-02"))
# print(date_between_start_end("2019-02-03", "2019-03-02"))

# print first_day_of_month(-12)
# print first_day_of_month(-11)
# print first_day_of_month(-10)
# print first_day_of_month(-9)
# print first_day_of_month(-8)
# print first_day_of_month(-7)
# print first_day_of_month(-6)
# print first_day_of_month(-5)
# print first_day_of_month(-4)
# print first_day_of_month(-3)
# print first_day_of_month(-2)
# print first_day_of_month(-1)
# print first_day_of_month(0)
# print first_day_of_month(1)
# print first_day_of_month(2)
# print first_day_of_month(3)
# print first_day_of_month(4)
# print first_day_of_month(5)
# print first_day_of_month(6)
# print first_day_of_month(7)
# print first_day_of_month(8)
# print first_day_of_month(9)
# print first_day_of_month(10)
# print first_day_of_month(11)
# print first_day_of_month(12)
#
#
# print last_day_of_month(-12)
# print last_day_of_month(-11)
# print last_day_of_month(-10)
# print last_day_of_month(-9)
# print last_day_of_month(-8)
# print last_day_of_month(-7)
# print last_day_of_month(-6)
# print last_day_of_month(-5)
# print last_day_of_month(-4)
# print last_day_of_month(-3)
# print last_day_of_month(-2)
# print last_day_of_month(-1)
# print last_day_of_month(0)
# print last_day_of_month(1)
# print last_day_of_month(2)
# print last_day_of_month(3)
# print last_day_of_month(4)
# print last_day_of_month(5)
# print last_day_of_month(6)
# print last_day_of_month(7)
# print last_day_of_month(8)
# print last_day_of_month(9)
# print last_day_of_month(10)
# print last_day_of_month(11)
# print last_day_of_month(12)



# print last_day_of_month(1)
#
# print start_day_of_month()
# print last_day_of_month()
#
# print start_day_of_month(-1)
# print last_day_of_month(-1)

# print last_day_of_current_month()

# print last_day_of_month(datetime.date(2002, 1, 17))

'''
print last_day_of_month(datetime.date(2012, month, 1))
>>> last_day_of_month(datetime.date(2002, 1, 17))
datetime.date(2002, 1, 31)
'''

# print hour()

# for i in range(100):
#     szText = "{} {}".format(i + 1, start_end_of_week(2019, i))
#     print(szText)