import numpy as np
import pandas as pd

from climatepix.utils.period import get_months_first_day, get_years_first_day, get_all_days_in_period


def construct_climate_dataframe(
    coords: list, period: str, climate_values: list, aggregation_level: str
) -> pd.DataFrame:
    coords_flat, days_flat, climate_values_flat = [], [], []

    if aggregation_level == "Yearly":
        coords_flat, days_flat = flatten_for_yearly(coords, period)

    elif aggregation_level == "Monthly":
        days_of_months = get_months_first_day(period)
        coords_flat, days_flat = flatten_for_monthly(coords, days_of_months)

    else:
        days_of_years = get_all_days_in_period(period)
        coords_flat, days_flat = flatten_for_daily(coords, days_of_years)

    climate_values_flat = flatten_climate_values(coords, climate_values, aggregation_level)
    
    df = pd.DataFrame({
        'x': [coord[0] for coord in coords_flat],
        'y': [coord[1] for coord in coords_flat],
        'day': days_flat,
        'value': climate_values_flat
    })

    return df


def flatten_for_yearly(coords, period):
    days = get_years_first_day(period)
    coords_flat = [coord for coord in coords for _ in days]
    days_flat = days * len(coords)
    return coords_flat, days_flat


def flatten_for_monthly(coords, months_of_years):
    coords_flat, days_flat = [], []
    for coord in coords:
        for months in months_of_years:
            coords_flat.extend([coord])
            days_flat.append(months)
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

    return np.array(climate_values_flat, dtype=np.float32)