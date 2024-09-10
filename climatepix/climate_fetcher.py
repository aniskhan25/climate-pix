import os
import pandas as pd
import rasterio as rio

from pyproj import CRS
from climatepix.utils.urls import build_url
from climatepix.utils.output import construct_climate_dataframe
from climatepix.utils.coords import reproject_coords, transform_coords
from climatepix.utils.period import (
    get_years,
    period_to_days,
    get_day_of_year,
    get_days_of_year,
    get_months_of_year,
)


def get_daily_climate_single(url: str, coords: list, bands: int) -> list:
    with rio.open(url) as dataset:
        src_crs = rio.crs.CRS.from_string("EPSG:4326")
        dst_crs = dataset.crs.to_proj4()
        new_coords = reproject_coords(src_crs, dst_crs, coords)
        return list(rio.sample.sample_gen(dataset, new_coords, indexes=bands))


def get_daily_climate(coords: list, period: str, climatic_var: str, aggregation_level: str) -> pd.DataFrame:
    years = get_years(period)
    days = period_to_days(period)

    urls = [build_url(climatic_var, year, aggregation_level=aggregation_level) for year in years]
    
    days_of_years = [get_days_of_year(days, year) for year in years]

    climate_values = []
    for url, day_data in zip(urls, days_of_years):
        if aggregation_level == "Yearly":
            values = get_daily_climate_single(url, coords, [1])
        elif aggregation_level == "Monthly":
            months = get_months_of_year(day_data)
            values = get_daily_climate_single(url, coords, months)
        else:
            days = get_day_of_year(day_data)
            values = get_daily_climate_single(url, coords, days)
        climate_values.extend(values)

    return {"days_of_years": days_of_years, "values": climate_values}


def fetch_climate_data(
    coords: list = None,
    climatic_vars: list = ["Prcp"],
    period: str = "2000-12-31:2001-01-03",
    output_dir: str = "climatepix/output",
    output_fn: str = "climate_values_df.csv",
    coords_df: pd.DataFrame = None,
    input_crs: str = "EPSG:4326",
    aggregation_level: str = "All"
) -> pd.DataFrame:
    dst_crs = CRS.from_epsg(4326)  # WGS84 Longitude/Latitude
    src_crs = CRS.from_string(input_crs)

    if coords_df is not None:
        coords = extract_coords_from_df(coords_df)
    elif coords is None:
        raise ValueError("Either coords or coords_df must be provided.")

    transformed_coords = transform_coords(coords, src_crs, dst_crs)

    all_climate_data = pd.DataFrame()

    for climatic_var in climatic_vars:
        raw_climate_data = get_daily_climate(transformed_coords, period, climatic_var, aggregation_level)

        climate_values_df = construct_climate_dataframe(
            coords,
            raw_climate_data["days_of_years"],
            raw_climate_data["values"],
            aggregation_level
        )

        climate_values_df.rename(columns={"value": climatic_var}, inplace=True)

        if all_climate_data.empty:
            all_climate_data = climate_values_df
        else:
            all_climate_data = pd.merge(
                all_climate_data,
                climate_values_df,
                on=list(climate_values_df.columns.difference([climatic_var])),
            )

    save_to_csv(all_climate_data, output_dir, output_fn)

    return all_climate_data


def extract_coords_from_df(coords_df: pd.DataFrame) -> list:
    if coords_df.shape[1] < 2:
        raise ValueError("precomputed_df must have at least two columns representing coordinates.")
    return list(coords_df.iloc[:, :2].itertuples(index=False, name=None))


def save_to_csv(df: pd.DataFrame, output_dir: str, output_fn: str):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_fn)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    coords = pd.DataFrame([[473245.00402982143, 6980252.896166361], [473245.00402982143, 6880252.896166361], [473245.00402982143, 6880252.896166361]], columns=['x', 'y'])
    climate_values_df = fetch_climate_data(
        coords_df=coords, 
        input_crs="EPSG:3067", 
        period="2017-01-01:2017-01-31", 
        aggregation_level="Monthly",
        climatic_vars=["Tmax", "Tmin", "Prcp"]
    )
    print(climate_values_df)