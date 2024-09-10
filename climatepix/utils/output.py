import pandas as pd

from climatepix.utils.period import get_months_of_year


def construct_climate_dataframe(
    coords: list, days_of_years: list, climate_values: list, aggregation_level: str
) -> pd.DataFrame:
    period_title, coords_flat, days_flat, climate_values_flat = "", [], [], []

    if aggregation_level == "Yearly":
        coords_flat, days_flat = flatten_for_yearly(coords, days_of_years)

    elif aggregation_level == "Monthly":
        coords_flat, days_flat = flatten_for_monthly(coords, days_of_years)

    else:
        coords_flat, days_flat = flatten_for_daily(coords, days_of_years)

    climate_values_flat = flatten_climate_values(coords, climate_values, aggregation_level)

    df = pd.DataFrame({
        'x': [coord[0] for coord in coords_flat],
        'y': [coord[1] for coord in coords_flat],
        'day': days_flat,
        'value': climate_values_flat
    })

    return df


def flatten_for_yearly(coords, days_of_years):
    days = [days[0] for days in days_of_years]
    coords_flat = [coord for coord in coords for _ in days]
    days_flat = days * len(coords)
    return coords_flat, days_flat


def flatten_for_monthly(coords, days_of_years):
    coords_flat, days_flat = [], []
    months_of_years = [get_months_of_year(days) for days in days_of_years]
    for coord in coords:
        for i, months in enumerate(months_of_years):
            coords_flat.extend([coord] * len(months))
            days_flat.append(days_of_years[i][0])
    return coords_flat, days_flat


def flatten_for_daily(coords, days_of_years):
    coords_flat, days_flat = [], []
    for coord in coords:
        for days in days_of_years:
            coords_flat.extend([coord] * len(days))
            days_flat.extend(days)
    return coords_flat, days_flat


def flatten_climate_values(coords, climate_values, aggregation_level):
    climate_values_flat = []
    num_items = len(climate_values) // len(coords)

    for i in range(len(coords)):
        for j in range(num_items):
            climate_values_flat.extend(climate_values[j * len(coords) + i])

    return climate_values_flat
