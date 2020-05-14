import importlib.util
import os

import sys


def _configure_methods() -> dict:
    _methods = {
        'env': lambda s: os.environ[s],
    }
    _configure_secret_manager(_methods)
    return _methods


def _extras_load(name: str) -> bool:
    if name in sys.modules:
        return True
    if (spec := importlib.util.find_spec(name)) is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        print(f"{name!r} feature available.")
        return True
    print(f'{name!r} feature not available.')
    return False

# noinspection PyUnresolvedReferences
def _configure_secret_manager(methods: dict):
    def _gsecrets(coords: str) -> str:
        parts = coords.split('/')
        if len(parts) < 2:
            raise Exception(f'Need project and secret name for method "gs", got {coords}.')
        project, secret, version = parts
        path = f'projects/{project}/secrets/{secret}/'
        if version is not None:
            path += f'versions/{version}/'
        secret = secrets.access_secret_version(path).payload.data.decode("utf-8")
        return secret

    if _extras_load('google.cloud.secretmanager'):
        secrets = secretmanager.SecretManagerServiceClient()
        methods['gs']: lambda s: _gsecrets(s)
