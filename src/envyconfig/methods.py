import os
from types import LambdaType
from typing import Dict

Methods = Dict[str, LambdaType]


def _configure_methods(configure_methods: bool) -> dict:
    if not configure_methods:
        return {}
    methods = {
        'env': lambda s: os.environ[s],
    }
    methods.update(_configure_secret_manager())
    return methods


def _gsecrets(secrets, coords: str) -> str:
    if coords[0] != '/':
        raise Exception(f'ERR: Unrecognized GS coordinate {coords}.')
    parts = coords[1:].split('/')
    if len(parts) < 2:
        raise Exception(f'Need project and secret name for method "gs", got {coords}.')
    path = f'projects/{parts[0]}/secrets/{parts[1]}/'
    if len(parts) == 3:
        path += f'versions/{parts[2]}/'
    secret = secrets.access_secret_version(path).payload.data.decode("utf-8")
    return secret


def _configure_secret_manager() -> Methods:
    try:
        from google.cloud import secretmanager
        secrets = secretmanager.SecretManagerServiceClient()
    except NameError:
        return {'gs': lambda s: f'ERR: Optional extra "google.cloud.secretmanager" is not available.'}
    except Exception as e:
        return {'gs': lambda s: f'ERR: {e}'}
    return {'gs': lambda s: _gsecrets(secrets, s)}
