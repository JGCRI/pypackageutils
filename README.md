[![build](https://github.com/JGCRI/pypackageutils/actions/workflows/build.yml/badge.svg)](https://github.com/JGCRI/pypackageutils/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/JGCRI/pypackageutils/branch/master/graph/badge.svg?token=VLNPBO7T2U)](https://codecov.io/gh/JGCRI/pypackageutils)

# pypackageutils
Common utilities used in Python modeling software packages

## Installation

The easiest way to install `pypackageutils` is using pip

```bash
pip install pypackageutils
```

## Functionality

Current features:
- `download_unpack_zip()`:  Download and unpack example zipped file with .zip extension to a user-specified location
- `download_file()`:  Download file and name and save it to a user-specified location
- `fetch_unpack_data()`:  Download and unpack example data supplement from Zenodo that matches the current installed distribution
- `remote_read()`:  Read in a file in table format from a remote source. Currently this function only works with .csv and .txt files.
