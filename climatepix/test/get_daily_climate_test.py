from climatepix.climate_fetcher import fetch_climate_data


def test_get_daily_climate_one():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climatic_var = "Prcp"

    period = "2001-01-01:2001-01-03"

    df = fetch_climate_data(coords=coords, period=period, climatic_var=climatic_var)

    assert df.shape == (6, 4)


def test_get_daily_climate_two():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climatic_var = "Prcp"

    period = "2001-12-31:2002-01-03"

    df = fetch_climate_data(coords=coords, period=period, climatic_var=climatic_var)

    assert df.shape == (8, 4)
