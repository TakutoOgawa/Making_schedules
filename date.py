import datetime

def today_date():
    date = str(datetime.date.today())
    return [int(date[0: 4]), int(date[5: 7]), int(date[8: 10])]

def weekday_of_the_first_day(year, month):
    year = int(year)
    month = int(month)
    diff = [1, -2, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    if year % 4 == 0:
        diff[1] += 1
    x = 5
    x += 365 * (year - 2000) + (year - 1997) // 4

    for i in range(month - 1):
        x += 30 + diff[i]

    x %= 7
    final_day = 30 + diff[month - 1]
    return x, final_day

def make_day_id(year, month, day, class_num):
    return str(year) + str(month).zfill(2) + str(day).zfill(2) + str(class_num)