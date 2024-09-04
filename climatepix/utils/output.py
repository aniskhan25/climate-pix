import pandas as pd


def construct_df(coords, days, climate_values):
    lat_list, lon_list, day_list, value_list = [], [], [], []

    for i, coord in enumerate(coords):
        lat, lon = coord

        lat_list.extend([lat] * len(days)) # Repeat lat, lon for each day in the period
        lon_list.extend([lon] * len(days))

        day_list.extend(days) # Repeat day for each coordinate

        climate_vals = climate_values[i]
        value_list.extend(climate_vals)

    df = pd.DataFrame({"lat": lat_list, "lon": lon_list, "day": day_list, "value": value_list})
    return df
