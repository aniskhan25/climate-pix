import os

import rasterio as rio
import pandas as pd

from utils.urls import build_url
from utils.output import construct_df
from utils.coords import reproject_coords
from utils.period import (
    get_years,
    period_to_days,
    get_day_of_year,
    get_days_of_year,
)


def get_daily_climate_single(url, coords, day_of_year):
    with rio.open(url) as dataset:
        src_crs = rio.crs.CRS.from_string("EPSG:4326")
        dst_crs = dataset.crs.to_proj4()

        new_coords = reproject_coords(src_crs, dst_crs, coords)
        values = list(rio.sample.sample_gen(dataset, new_coords, day_of_year))
    return values


def get_daily_climate(coords, period="2001-01-01:2001-01-03", climatic_var="Prcp"):
    years = get_years(period)
    days = period_to_days(period)

    urls = [build_url(climatic_var, year) for year in years]

    climate_values_dataframes = []  # List to store DataFrames for each url
    for index, url in enumerate(urls):
        days_of_year = get_days_of_year(days, years[index])
        day_of_year = get_day_of_year(days_of_year)

        values = get_daily_climate_single(url, coords, day_of_year)  # value[0] == band 1 value at lon, lat

        climate_values_df = construct_df(coords, days_of_year, values)
        climate_values_dataframes.append(climate_values_df)

    merged_climate_values_df = pd.concat(climate_values_dataframes, axis=0)
    return merged_climate_values_df


def main(
    coords=None,
    climatic_var="Prcp",
    period="2001-01-01:2001-01-03",
    output_dir="climatepix/output",
    output_fn="climate_values_df.csv",
    precomputed_df=None,
):
    if precomputed_df is not None:
        if precomputed_df.shape[1] < 2:
            raise ValueError("precomputed_df must have at least two columns representing coordinates.")

        coords = list(zip(precomputed_df.iloc[:, 0], precomputed_df.iloc[:, 1]))
    elif coords is None:
        raise ValueError("Either coords or precomputed_df must be provided.")

    climate_values_df = get_daily_climate(coords, period, climatic_var)

    os.makedirs(output_dir, exist_ok=True)

    climate_values_df.to_csv(
        os.path.join(os.getcwd(), output_dir, output_fn),
        index=False,  # Set to True if you want to include row indices in the output file
    )

    return climate_values_df


if __name__ == "__main__":
    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude] not [lat, lon]...

    climate_values_df = main(coords)

    print(climate_values_df.shape)
