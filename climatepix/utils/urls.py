def build_url(climatic_var_single, year, version=4, aggregation_level="All"):

    if aggregation_level not in ["Monthly", "Yearly", "All"]:
        raise ValueError(f"Invalid aggregation level '{aggregation_level}'. Available options are 'Yearly', 'Monthly' or 'All'.")

    if climatic_var_single not in ["Tmax", "Tmin", "Prcp"]:
        raise ValueError(f"Invalid climatic_var_single '{climatic_var_single}'. Available options are 'Tmax', 'Tmin' or 'Prcp'.")

    if version == 3:
        if not (1950 <= year <= 2020):
            raise ValueError("Year (period) must be between 1950 and 2020")
    elif version == 4:
        if not (1950 <= year <= 2022):
            raise ValueError("Year (period) must be between 1950 and 2022")
    else:
        raise ValueError("Invalid version number")

    climvar = {"Tmax": "tmax", "Tmin": "tmin", "Prcp": "prec"}[climatic_var_single]

    if climatic_var_single == "Prcp":
        value_type = "Sum"
    else:
        value_type = "Avg"
    
    if aggregation_level == "All":
        url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/{aggregation_level}DataRasters/{climvar}/Downscaled{climatic_var_single}{year}_cogeo.tif"    
    else:
        url = f"ftp://palantir.boku.ac.at/Public/ClimateData/v{version}_cogeo/{aggregation_level}DataRasters/{climvar}/Downscaled{climatic_var_single}{year}{aggregation_level}{value_type}_cogeo.tif"

    return url
