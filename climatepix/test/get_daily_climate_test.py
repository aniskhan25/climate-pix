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


def test_get_daily_climate_three():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climatic_var = "Prcp"

    period = "2002-01-31:2002-02-03"

    df = fetch_climate_data(coords=coords, period=period, climatic_var=climatic_var, aggregation_level="All")

    assert df.shape == (8, 4)


def test_get_daily_climate_four():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climatic_var = "Prcp"

    period = "2001-12-31:2002-01-03"

    df = fetch_climate_data(coords=coords, period=period, climatic_var=climatic_var, aggregation_level="Monthly")

    assert df.shape == (4, 4)


def test_get_daily_climate_five():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude]

    climatic_var = "Prcp"

    period = "2001-12-31:2002-01-03"

    df = fetch_climate_data(coords=coords, period=period, climatic_var=climatic_var, aggregation_level="Yearly")

    assert df.shape == (4, 4)
