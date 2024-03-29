# envyconfig
Envyconfig is a python package for reading YAML config files with pointers to external keys.  It reads the specified YAML file, fetches data from the configured sources, and returns the corresponding dict structure.

The primary purpose is to allow keys to secret configuration items to be stored in the YAML file, for ease of use during program loading.

Builds on the PyYAML package, with the following additions:
* Environment variables can be specified as config values.
* GCP Secrets can be specified as config values.
* Nested YAML structures can be flattened to get a simple key / value dict.
* Default values can be specified, for instance from the command line.

Requires Python 3.8 or higher.


## Basic Usage

```python
>> > import envyconfig
>> > config = envyconfig.load(config_file='my_config.yaml')
>> > print(config)
{'foo': {'bar': 'baz'}}
```

### Sample config file.
```yaml
foo:

   # Google Cloud Secret Manager: Loads "bar" from secret "bar" in the "my-project"
   #  GCP project.
   bar: ${gs:/my-project/my-secret}

   # Environment variables: Loads "baz" from the environment variable "BAZ".
   # If this variable is not set, it defaults to "something_else".
   baz: ${env:BAZ:something_else}

   # HashiCorp Vault: Loads "bam" from the secret "bam" mounted Vault mount
   # "/path/to/secrets/mount/my-secrets/".
   bam: ${vault:/path/to/secrets/mount/my-secrets/bam}
```


## Usage Details
### Interpolation keys.
You indicate the values you want interpolated by one of the configured engines through a wrapper
`${<method>:<key>:<default>}`, such as `${env:MY_VAR:my_default}`.  The currently supported engines are
* environment (`os.environ`) variables (key: `env`), and
* Google Secret Manager (key: `gs`).
* HashiCorp Vault
* Format strings for run-time interpolation.
The engines are lazy-loaded, so unless you request interpolation by one of them, the configuration is not loaded.
This is useful for advanced engines (presently `gs`), that rely on external libraries and configuration.

As the method, key and default values are separated by a `:`, this character is not allowed in the method or
key names.  It is allowed in default values, though.  So `$(env:REDIRECT_PAGE:https://localhost/}` is legal syntax.

### Environment variables
Environment variables behave like you expect them to.

### Google Secret Manager
This engine requires the optional dependency (or separate installation of) `google-cloud-secret-manager`
(i.e. `pip install envyconfig[google-cloud-secret-manager]`), and a pointer to your GCP key
(`GOOGLE_APPLICATION_CREDENTIALS`), as described on [Authenticating as a service account](https://cloud.google.com/docs/authentication/production))

#### Credits and further documentation
* [GCP Python Secret Manager](https://github.com/googleapis/python-secret-manager)
* [Python Environment Variables](https://docs.python.org/3/using/cmdline.html#environment-variables)
* [HashiCorp Vault](https://www.vaultproject.io/)
* [PyYAML](https://pyyaml.org)
* [EnvyConfig](https://github.com/geirem/envyconfig/)
