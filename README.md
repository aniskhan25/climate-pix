
# Climate-Pix Repository

Welcome to the Climate-Pix repository! This repository serves as a hub for accessing high-resolution daily climate data for Europe from the European climatic database hosted at [University of Natural Resources and Life Sciences, Vienna, Austria](https://boku.ac.at/en/wabo/waldbau/wir-ueber-uns/daten).

## Overview

Climate-Pix provides high-resolution (1 km) daily climate data, including precipitation, minimum and maximum temperatures, sourced from the European climatic database. This dataset covers Europe and spans from 1950 to 2022. The dataset was originally built by [A. Moreno & H. Hasenauer](https://doi.org/10.1002/joc.4436) and further developed by W. Rammer, C. Pucher & M. Neumann.

## Features

- **High-resolution Data:** Climate-Pix offers access to high-resolution (1 km) daily climate data for Europe, sourced from the European climatic database hosted at [University of Natural Resources and Life Sciences, Vienna, Austria](https://boku.ac.at/en/wabo/waldbau/wir-ueber-uns/daten).

## Usage

To utilize the Climate-Pix dataset, follow this step:  

1. **Install package:**

```bash
pip install climatepix@git+https://github.com/aniskhan25/climate-pix.git
```

2. **Example:**

```python
import pandas as pd

from climatepix.climate_fetcher import fetch_climate_data

coords = {
    'x': [26.47267087598713, 26.488284622109926],
    'y': [62.951120658250794, 62.053564877176285]
}
coords_df = pd.DataFrame(coords)

climate_values_df = fetch_climate_data(coords_df=coords_df)
```

## Getting Started (Mac OS, for development)
  
```bash
git clone https://github.com/aniskhan25/climate-pix.git
cd climate-pix

python3 -m venv venv

source venv/bin/activate

pip install -e .
```

## License

The Climate-Pix repository is provided under the [GNU General Public License](LICENSE). Feel free to use the data for personal, academic, or commercial purposes, with proper attribution.

## Contact

If you have any questions or feedback regarding Climate-Pix, please don't hesitate to [contact us](mailto:aniskhan25@gmail.com). We're here to help!
