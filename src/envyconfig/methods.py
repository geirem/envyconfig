import os
from types import LambdaType
from typing import Dict, Callable

from src.envyconfig.exceptions.ConfigurationError import ConfigurationError
from src.envyconfig.exceptions.SecretNotFoundError import SecretNotFoundError

Methods = Dict[str, Callable]

_methods = {}


def _configure_methods(method: str) -> LambdaType:
    if method in _methods:
        return _methods[method]
    if 'env' == method:
        _methods.update({'env': lambda s: None if not s in os.environ else os.environ[s]})
    if 'gs' == method:
        _methods.update(_configure_gcp_secret_manager())
    if 'vault' == method:
        _methods.update(_configure_hashicorp_vault())
    return _methods[method]


def _gcp_secrets(secrets, coords: str) -> str:
    if coords[0] != '/':
        raise Exception(f'ERR: Unrecognized GS coordinate {coords}.')
    parts = coords[1:].split('/')
    if len(parts) not in [2, 3]:
        raise Exception(f'Need project and secret name, and optional version, for method "gs", got {coords}.')
    version = 1 if len(parts) == 2 else parts[2]
    path = f'projects/{parts[0]}/secrets/{parts[1]}/versions/{version}'
    return secrets.access_secret_version(path).payload.data.decode("utf-8")


def _configure_gcp_secret_manager() -> Methods:
    try:
        from google.cloud import secretmanager
        from google.auth.exceptions import DefaultCredentialsError
        secrets = secretmanager.SecretManagerServiceClient()
    except NameError:
        raise Exception('ERR: Requested extra "google.cloud.secretmanager" is not available.')
    return {'gs': lambda s: _gcp_secrets(secrets, s)}


def _configure_hashicorp_vault() -> Methods:
    import requests
    _seen_coords = {}

    def vault_broker(coords: str) -> str:
        parts = coords.split('?')
        if len(parts) > 2:
            raise Exception('ERR: Expected path and version to be separated by a single "?" char.')
        path = parts[0]
        mount, secret, key = path.rsplit('/', 2)
        url = f'{vault_addr}{mount}/data/{secret}'
        if len(parts) == 2:
            url += f'?version={parts[1]}'
        if url not in _seen_coords:
            response = requests.get(url, headers={'X-Vault-Token': vault_token})
            if response.status_code == 403:
                raise ConfigurationError("ERR: Wrong Vault token for this mount.")
            if response.status_code == 404:
                raise SecretNotFoundError(f'ERR: HashiCorp Vault secret path {url} not found.')
            if response.status_code != 200:
                raise Exception('ERR: Unable to fetch from HashiCorp Vault.')
            results = response.json()['data']['data']
            _seen_coords[url] = results
        if key not in (s_map :=_seen_coords[url]):
            raise SecretNotFoundError(f'ERR: HashiCorp Vault secret {key} not found at {coords}.')
        return s_map[key]

    vault_addr, vault_token = os.environ['VAULT_ADDR'], os.environ['VAULT_TOKEN']
    if not vault_addr or not vault_token:
        raise ConfigurationError('Missing configuration for Vault integration: VAULT_ADDR and VAULT_TOKEN must be set.')
    return {'vault': lambda c: vault_broker(c)}


def _hashicorp_vault(vault_broker, coords: str) -> str:
    return vault_broker.fetch(coords)
