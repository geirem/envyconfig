# envyconfig
Envyconfig is a python package for reading YAML config files with pointers to external keys.  It reads the specified YAML file, fetches data from the configured sources, and returns the corresponding dict structure.

The primary purpose is to allow keys to secret configuration items to be stored in the YAML file, for ease of use during program loading.

Builds on the PyYAML package, with the following additions:
* Environment variables can be specified as config values.
* GCP Secrets can be specified as config values.
* Nested YAML structures can be flattened to get a simple key / value dict.
* Default values can be specified, for instance from the command line.


## Basic Usage
```python
>>> import envyconfig
>>> config = envyconfig.load('config.yaml')
>>> print(config)
{'foo': {'bar': 'baz'}}
```

### Sample config file.
```yaml
foo:
   # Loads "bar" from secret "my-secret" in the "my-project" GCP project.  Defaults to "otherwise".
   bar: ${gs:/my-project/my-secret:otherwise}
   # Loads "baz" from the environment variable "ENVVAR".  Defaults to "something_else".
   baz: ${env:ENVVAR:something_else}
```


## Usage Details
### Interpolation keys.
You indicate the values you want interpolated by one of the configured engines through a wrapper
`${<method>:<key>:<default>}`, such as `${env:MY_VAR:my_default}`.  The currently supported engines are
* environment (`os.environ`) variables (key: `env`), and
* Google Secret Manager (key: `gs`).
The engines are lazy-loaded, so unless you request interpolation by one of them, the configuration is not loaded.
This is useful for advanced engines (presently `gs`), that rely on external libraries and configuration.

As the method, key and default values are separated by a `:`, this character is not allowed in the method or
key names.  It is allowed in default values, though.  So `$(env:REDIRECT_PAGE:https://localhost/}` is legal syntax.

### Environment variables
Environment variables behave like you expect them to.

### Google Secret Manager
This engine requires the optional dependency (or separate installation of) `googlesecrets`
(ie. `pip install envyconfig[googlesecrets]`), and a pointer to your GCP key (`GOOGLE_APPLICATION_CREDENTIALS`) with
the appropriate credentials.

#### Credits and further documentation
* [GCP Python Secret Manager](https://github.com/googleapis/python-secret-manager)
* [PyYAML](https://pyyaml.org)
* [EnvyConfig](https://github.com/geirem/envyconfig/)
