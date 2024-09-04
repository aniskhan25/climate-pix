from access.get_daily_climate import get_daily_climate


def test_get_daily_climate_one():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude] not [lat, lon]...

    climatic_var = "Prcp"

    period = "2001-01-01:2001-01-03"

    df = get_daily_climate(coords, period, climatic_var)

    assert df.shape == (6, 4)


def test_get_daily_climate_two():

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude] not [lat, lon]...

    climatic_var = "Prcp"

    period = "2001-12-31:2002-01-03"

    df = get_daily_climate(coords, period, climatic_var)

    assert df.shape == (8, 4)
