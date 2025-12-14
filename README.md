# Welcome to pooch-dataverse

[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ssciwr/pooch-dataverse/ci.yml?branch=main)](https://github.com/ssciwr/pooch-dataverse/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/pooch-dataverse/badge/)](https://pooch-dataverse.readthedocs.io/)
[![codecov](https://codecov.io/gh/ssciwr/pooch-dataverse/branch/main/graph/badge.svg)](https://codecov.io/gh/ssciwr/pooch-dataverse)

## Installation

The Python package `pooch_dataverse` can be installed from PyPI:

```
python -m pip install pooch_dataverse
```

## Development installation

If you want to contribute to the development of `pooch_dataverse`, we recommend
the following editable installation from this repository:

```
git clone https://github.com/ssciwr/pooch-dataverse
cd pooch-dataverse
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
