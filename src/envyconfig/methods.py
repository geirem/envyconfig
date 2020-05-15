import os
from types import LambdaType
from typing import Dict, List, Callable

Methods = Dict[str, LambdaType]

_methods = {}


def _configure_methods(method: str) -> Callable:
    if method in _methods:
        return _methods[method]
    if 'env' == method:
        _methods.update({'env': lambda s: None if not s in os.environ else os.environ[s]})
    if 'gs' == method:
        _methods.update(_configure_secret_manager())
    return _methods[method]


def _gsecrets(secrets, coords: str) -> str:
    if coords[0] != '/':
        raise Exception(f'ERR: Unrecognized GS coordinate {coords}.')
    parts = coords[1:].split('/')
    if len(parts) not in [2, 3]:
        raise Exception(f'Need project and secret name, and optional version, for method "gs", got {coords}.')
    version = 1 if len(parts) == 2 else parts[2]
    path = f'projects/{parts[0]}/secrets/{parts[1]}/versions/{version}'
    return secrets.access_secret_version(path).payload.data.decode("utf-8")


def _configure_secret_manager() -> Methods:
    try:
        from google.cloud import secretmanager
        from google.auth.exceptions import DefaultCredentialsError
        secrets = secretmanager.SecretManagerServiceClient()
    except NameError:
        raise Exception('ERR: Requested extra "google.cloud.secretmanager" is not available.')
    return {'gs': lambda s: _gsecrets(secrets, s)}
