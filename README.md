# pyconfig
Python package for YAML config files.  Reads a specified YAML file, and returns the corresponding dict structure.

Builds on the PyYAML package, with the following additions:
* Environment variables can be specified as config values.
* Nested YAML structures can be flattened get a simple key / value dict.
* Default values can be specified, for instance from the command line.


## Usage
```python
>>> import envyconfig
>>> config = envyconfig.load('config.yaml')
>>> print(config)
{'foo': {'bar': 'baz'}}
```
