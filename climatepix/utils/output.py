import pandas as pd


def construct_df(coords, days, climate_values):
    x_list, y_list, day_list, value_list = [], [], [], []

    for i, coord in enumerate(coords):
        x, y = coord

        x_list.extend([x] * len(days)) # Repeat x, y for each day in the period
        y_list.extend([y] * len(days))

        day_list.extend(days) # Repeat day for each coordinate

        climate_vals = climate_values[i]
        value_list.extend(climate_vals)

    df = pd.DataFrame({"x": x_list, "y": y_list, "day": day_list, "value": value_list})
    return df
