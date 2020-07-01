import os
from types import LambdaType
from typing import Dict, Callable

from src.envyconfig.exceptions.ConfigurationError import ConfigurationError
from src.envyconfig.lib.VaultBroker import VaultBroker

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
    vault_addr, vault_token = os.environ['VAULT_ADDR'], os.environ['VAULT_TOKEN']
    if not vault_addr or not vault_token:
        raise ConfigurationError('Missing configuration for Vault integration: VAULT_ADDR and VAULT_TOKEN must be set.')
    vault_broker = VaultBroker(vault_addr, vault_token)
    return {'vault': lambda c: vault_broker(c)}


def _hashicorp_vault(vault_broker, coords: str) -> str:
    return vault_broker.fetch(coords)
