# ATM-Aux

## OpenML collection

OpenML collection script requires the `requests` python package. Install with pip by `pip install requests`.

## ModelHub API

The `modelhub_api` folder allows exploration of the classifiers in ModelHub. In order to run the API, first install the requirements by entering the `modelhub_api` folder with `pip install -r requirements`.

The CSV can be downloaded from AWS S3 by running the `download_csvs_from_s3.py` script. It is run by the command `python download_csvs_from_s3.py`. The CSV will be stored in `gp_csvs` and `grid_csvs` corresponding to the GP+Bandit and Grid runs from the [paper](https://cyphe.rs/static/atm.pdf).

The `modelhub-api-test.py` scipt shows an example of how to use the API. It can be run with the command `python modelhub-api-test.py -r gp` or `python modelhub-api-test.py -r grid`.

