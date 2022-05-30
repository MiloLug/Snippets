## Requirements

Systemwide:
```bash
pip install -U setuptools wheel twine
```

## Build

From the root dir of the package:

```bash
# to build the package
python setup.py sdist bdist_wheel

# to install it locally
pip install -e .
```

To publish:
```bash
# test
twine upload --repository testpypi dist/*
# prod
twine upload dist/*
```

### Don't forget to update the version number in `setup.py`!