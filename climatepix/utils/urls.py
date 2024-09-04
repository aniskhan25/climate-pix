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

    climvar = {"Tmax": "tmax", "Tmin": "tmin", "Prcp": "prec"}[climatic_var_single]

    url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/AllDataRasters/{climvar}/Downscaled{climatic_var_single}{year}_cogeo.tif"
    return url
