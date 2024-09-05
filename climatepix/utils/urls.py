def build_url(climatic_var_single, year, version=4, aggregation_level="daily"):

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

    if aggregation_level == "yearly":
        url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/YearlyDataRasters/{climvar}/Downscaled{climatic_var_single}{year}YearlySum_cogeo.tif"

    elif aggregation_level == "monthly":
        url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/MonthlyDataRasters/{climvar}/Downscaled{climatic_var_single}{year}MonthlySum_cogeo.tif"

    elif aggregation_level == "daily":
        url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/AllDataRasters/{climvar}/Downscaled{climatic_var_single}{year}_cogeo.tif"
    
    else:
        raise ValueError(f"Invalid aggregation level '{aggregation_level}'. Available options are 'yearly', 'monthly' or 'daily'.")
    
    return url
