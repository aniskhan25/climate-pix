from datetime import datetime, timedelta


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
