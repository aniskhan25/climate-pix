"""Main module of climate-pix

Author(s): Anis Ur Rahman

This code is covered under the GNU General Public License v3.0.
Please refer to the LICENSE located in the root of this repository.
"""

import os

from access.get_daily_climate import get_daily_climate


if __name__ == "__main__":

    coords = [[-5.36, 37.40], [-5.3, 37.41]]  #  [longitude, latitude] not [lat, lon]...

    climatic_var = "Prcp"

    period = "2001-01-01:2001-01-03"

    climate_values_df = get_daily_climate(coords, period, climatic_var)

    # Write the climate values to a CSV file
    climate_values_df.to_csv(
        os.path.join(os.getcwd(), "climate-pix/output", "climate_values_df.csv"),
        index=False,  # Set to True if you want to include row indices in the output file
    )

    print(climate_values_df.shape)
