# Python Avri API

[![Build Status](https://dev.azure.com/timvancann/timvancann/_apis/build/status/timvancann.pyavri?branchName=master)](https://dev.azure.com/timvancann/timvancann/_build/latest?definitionId=1&branchName=master)
[![PyPI](https://img.shields.io/pypi/v/avri-api)](https://pypi.org/project/avri-api/)

Unofficial wrapper around the [Avri](https://avri.nl/) API, for automation purposes.

## Usage

```bash
pip install avri-api
```

Initialize the client with you `postal code` and `house number`. Optionally provide a `house_nr_extension` and/or a `country_code`.
```python
from avri.api import Avri
client = Avri('1234AB', 42)
```

Exposes the following functions:
- ```client.upcoming()``` returns first upcoming collecting day in a `Garbage` object
- ```client.upcoming_of_each()``` returns first upcoming collecting day for each garbage type in a `List[Garbage]` object
- ```client.all()``` returns all upcoming collecting days in a `List[Garbage]` object

Both `upcoming` and `upcoming_of_each` contain today's pickup.

### The `Garbage` object

Contains 
- `name`: The name of the garbage type, e.g. `plastic` or `gft`.
- `day`: A python datetime object representing the collecting date.

## In a long living process
Data is cached for `6` days before it's refreshed to reduce the number of API calls made.
