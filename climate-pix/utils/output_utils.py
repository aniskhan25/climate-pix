import pandas as pd


def construct_df(coords, days, climate_values):

    # Initialize empty lists for lat, lon, day, and value
    lat_list = []
    lon_list = []
    day_list = []
    value_list = []

    # Iterate through each coordinate
    for i, coord in enumerate(coords):
        lat, lon = coord
        # Repeat lat, lon for each day in the period
        lat_list.extend([lat] * len(days))
        lon_list.extend([lon] * len(days))

        # Repeat day for each coordinate
        day_list.extend(days)

        # Extract climate values for current coordinate
        climate_vals = climate_values[i]
        value_list.extend(climate_vals)

    # Create DataFrame
    df = pd.DataFrame(
        {"lat": lat_list, "lon": lon_list, "day": day_list, "value": value_list}
    )

    return df
