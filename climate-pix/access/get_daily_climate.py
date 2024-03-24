import os

import pandas as pd

import rasterio.sample

from utils.coords_utils import reproject_coords
from utils.period_utils import (
    get_years,
    period_to_days,
    get_day_of_year,
    get_days_of_year,
)
from utils.output_utils import construct_df


def build_url(climatic_var_single, year, version=4):

    if climatic_var_single not in ["Tmax", "Tmin", "Prcp"]:
        raise ValueError("climatic_var_single must be one of 'Tmax', 'Tmin' or 'Prcp'")

    if version == 3:
        if not (1950 <= year <= 2020):
            raise ValueError("Year (period) must be between 1950 and 2020")
    elif version == 4:
        if not (1950 <= year <= 2022):
            raise ValueError("Year (period) must be between 1950 and 2022")
    else:
        raise ValueError("Invalid version number")

    # Adjust climvar to file names
    climvar = {"Tmax": "tmax", "Tmin": "tmin", "Prcp": "prec"}[climatic_var_single]

    # Build URL
    url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/AllDataRasters/{climvar}/Downscaled{climatic_var_single}{year}_cogeo.tif"

    return url


def get_daily_climate_single(url, coords, day_of_year):

    with rasterio.open(url) as dataset:
        src_crs = rasterio.crs.CRS.from_string("EPSG:4326")
        dst_crs = (
            dataset.crs.to_proj4()
        )  # '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
        # dst_crs = dataset.crs.to_wkt()  # 'PROJCS["World_Mollweide",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS    84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mollweide"],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'

        new_coords = reproject_coords(src_crs, dst_crs, coords)

        values = list(rasterio.sample.sample_gen(dataset, new_coords, day_of_year))

    return values


def get_daily_climate(coords, period="2001-01-01:2001-01-03", climatic_var="Prcp"):

    years = get_years(period)

    days = period_to_days(period)

    urls = [build_url(climatic_var, year) for year in years]

    climate_values_dataframes = []  # List to store DataFrames for each url

    for index, url in enumerate(urls):

        days_of_year = get_days_of_year(days, years[index])

        day_of_year = get_day_of_year(days_of_year)

        values = get_daily_climate_single(
            url, coords, day_of_year
        )  # value[0] == band 1 value at lon, lat

        climate_values_df = construct_df(coords, days_of_year, values)

        climate_values_dataframes.append(climate_values_df)

    merged_climate_values_df = pd.concat(climate_values_dataframes, axis=0)

    return merged_climate_values_df
