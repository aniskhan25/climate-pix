import pandas as pd

from dateutil import parser
from datetime import datetime, timedelta
from collections import defaultdict


def get_years(period):
    days = period_to_days(period)
    years = sorted(set([datetime.strptime(day, "%Y-%m-%d").strftime("%Y") for day in days]))
    years = [int(year) for year in years]
    return years


def get_months_of_year(days):
    return list({datetime.strptime(day, "%Y-%m-%d").timetuple().tm_mon for day in days})


def get_day_of_year(days):
    return [datetime.strptime(day, "%Y-%m-%d").timetuple().tm_yday for day in days]


def get_days_of_year(days, year):
    return [day for day in days if day.startswith(str(year))]


def period_to_days(period):
    dates = period.split(":")
    if len(dates) == 1:
        ini = fin = dates[0]
    elif len(dates) == 2:
        ini, fin = dates
    else:
        raise ValueError("Invalid period format")

    ini = datetime.strptime(ini, "%Y-%m-%d")
    fin = datetime.strptime(fin, "%Y-%m-%d")

    days = [
        (ini + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((fin - ini).days + 1)
    ]

    return days


def get_all_days_in_period(period):
    start_date_str, end_date_str = period.split(":")
    
    start_date = parser.parse(start_date_str)
    end_date = parser.parse(end_date_str)
    
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    grouped_dates = defaultdict(list)
    for date in all_dates:
        year = date.year
        grouped_dates[year].append(date.strftime('%Y-%m-%d'))
    
    return list(grouped_dates.values())


def get_months_first_day(period):
    start_date_str, end_date_str = period.split(":")
    start_date = parser.parse(start_date_str)
    end_date = parser.parse(end_date_str)

    first_dates = []
    first_dates.append(start_date)

    next_month_start = (start_date + pd.DateOffset(months=1)).replace(day=1)

    if next_month_start <= end_date:
        first_dates.extend(pd.date_range(start=next_month_start, end=end_date, freq='MS'))

    first_dates_list = [d.strftime('%Y-%m-%d') for d in first_dates]

    return first_dates_list


def get_years_first_day(period):
    start_date_str, end_date_str = period.split(":")
    start_date = parser.parse(start_date_str)
    end_date = parser.parse(end_date_str)

    first_dates = []
    first_year_start = start_date.replace(month=1, day=1)
    first_dates.append(first_year_start)

    next_year_start = (first_year_start + pd.DateOffset(years=1)).replace(month=1, day=1)

    while next_year_start <= end_date:
        first_dates.append(next_year_start)
        next_year_start = next_year_start + pd.DateOffset(years=1)

    first_dates_list = [d.strftime('%Y-%m-%d') for d in first_dates]

    return first_dates_list
