import os

import numpy as np
import pandas as pd
import rasterio as rio

from pyproj import CRS

from climatepix.utils.urls import build_url
from climatepix.utils.output import construct_df
from climatepix.utils.coords import reproject_coords, transform_coords
from climatepix.utils.period import (
    get_years,
    period_to_days,
    get_day_of_year,
    get_days_of_year,
)


def get_daily_climate_single(url: str, coords: list, day_of_year: int) -> list:
    with rio.open(url) as dataset:
        src_crs = rio.crs.CRS.from_string("EPSG:4326")
        dst_crs = dataset.crs.to_proj4()

        new_coords = reproject_coords(src_crs, dst_crs, coords)
        return list(rio.sample.sample_gen(dataset, new_coords, indexes=day_of_year))


def get_daily_climate(coords: list, period: str, climatic_var: str) -> pd.DataFrame:
    years = get_years(period)
    days = period_to_days(period)

    urls = [build_url(climatic_var, year) for year in years]
    days_of_years = [get_days_of_year(days, year) for year in years]

    climate_values = []
    for url, days_of_year in zip(urls, days_of_years):
        values = get_daily_climate_single(url, coords, get_day_of_year(days_of_year))
        climate_values.extend(values)

    return {"days_of_years": days_of_years, "values": climate_values}


def construct_climate_dataframe(coords, days_of_years, climate_values) -> pd.DataFrame:
    coords_flat = []
    days_flat = []
    climate_values_flat = []

    # Flatten coordinates and days
    for i, coord in enumerate(coords):
        for days in days_of_years:
            num_days = len(days)
            coords_flat.extend([coord] * num_days)
            days_flat.extend(days)

    # Interleave climate values
    for i in range(len(coords)):
        for j in range(len(days_of_years)):
            climate_values_flat.extend(climate_values[j * len(coords) + i])

    df = pd.DataFrame({
        'x': [coord[0] for coord in coords_flat],
        'y': [coord[1] for coord in coords_flat],
        'day': days_flat,
        'value': climate_values_flat
    })

    return df

def fetch_climate_data(
    coords: list = None,
    climatic_var: str = "Prcp",
    period: str = "2000-12-31:2001-01-03",
    output_dir: str = "climatepix/output",
    output_fn: str = "climate_values_df.csv",
    coords_df: pd.DataFrame = None,
    input_crs: str = "EPSG:4326",
) -> pd.DataFrame:
    dst_crs = CRS.from_epsg(4326)  # WGS84 Longitude/Latitude
    src_crs = CRS.from_string(input_crs)

    if coords_df is not None:
        if coords_df.shape[1] < 2:
            raise ValueError("precomputed_df must have at least two columns representing coordinates.")

        coords = list(coords_df.iloc[:, :2].itertuples(index=False, name=None))
    elif coords is None:
        raise ValueError("Either coords or precomputed_df must be provided.")

    transformed_coords = transform_coords(coords, src_crs, dst_crs)

    raw_climate_data = get_daily_climate(transformed_coords, period, climatic_var)

    climate_values_df = construct_climate_dataframe(
        coords,
        raw_climate_data["days_of_years"],
        raw_climate_data["values"]
    )

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_fn)

    climate_values_df.to_csv(output_path, index=False)

    return climate_values_df


if __name__ == "__main__":
    '''
    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climate_values_df = fetch_climate_data(coords)
    '''
    coords = [[473245.00402982143, 6980252.896166361], [473245.00402982143, 6880252.896166361]]  # Example coordinates in EPSG:3067

    climate_values_df = fetch_climate_data(coords, input_crs="EPSG:3067")
    
    print(climate_values_df)
    