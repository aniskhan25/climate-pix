import os

import rasterio as rio
import pandas as pd

from climatepix.utils.urls import build_url
from climatepix.utils.output import construct_df
from climatepix.utils.coords import reproject_coords
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


def get_daily_climate(coords: list, period: str = "2001-01-01:2001-01-03", climatic_var: str = "Prcp") -> pd.DataFrame:
    years = get_years(period)
    days = period_to_days(period)

    urls = [build_url(climatic_var, year) for year in years]

    days_of_years = [get_days_of_year(days, year) for year in years]

    climate_values_dataframes = [
        construct_df(
            coords,
            days_of_year,
            get_daily_climate_single(url, coords, get_day_of_year(days_of_year))
        )
        for url, days_of_year in zip(urls, days_of_years)
    ]

    return pd.concat(climate_values_dataframes, axis=0)


def fetch_climate_data(
    coords: list = None,
    climatic_var: str = "Prcp",
    period: str = "2001-01-01:2001-01-03",
    output_dir: str = "climatepix/output",
    output_fn: str = "climate_values_df.csv",
    precomputed_df: pd.DataFrame = None,
) -> pd.DataFrame:
    if precomputed_df is not None:
        if precomputed_df.shape[1] < 2:
            raise ValueError("precomputed_df must have at least two columns representing coordinates.")

        coords = list(precomputed_df.iloc[:, :2].itertuples(index=False, name=None))
    elif coords is None:
        raise ValueError("Either coords or precomputed_df must be provided.")

    climate_values_df = get_daily_climate(coords, period, climatic_var)

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_fn)

    climate_values_df.to_csv(output_path, index=False)

    return climate_values_df


if __name__ == "__main__":
    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climate_values_df = fetch_climate_data(coords)

    print(climate_values_df.shape)
