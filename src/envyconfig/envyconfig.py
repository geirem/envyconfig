import os
from typing import Any, Tuple

from google.cloud import secretmanager

import yaml

from .exceptions import MissingInterpolationMethodException

_secrets = secretmanager.SecretManagerServiceClient()
_methods = {
    'env': lambda s: os.environ[s],
    'gs': lambda s: _secrets.access_secret_version(
        f"projects/dbd-sandbox-o9c/secrets/{s}/versions/1"
    ).payload.data.decode("utf-8")
}


def load(config_file: str, flatten: bool = False, override: dict = None):
    """
    :param config_file: Resolvable path of the YAML file containing the config.
    :param (optional) flat_map: Boolean value, truthy if you want to flatten the config file.
    :param (optional) override: Map of values to use instead of the config file.
    """
    with open(config_file) as inimage:
        config = yaml.safe_load(inimage)
    _interpolate_leafs(config)
    if flatten:
        config = _flatten(config)
    if override:
        config.update(override)
    return config


def _interpolate_leafs(config: dict) -> None:
    for child_key in config.keys():
        _replace_env(config, child_key)


def _flatten(config) -> dict:
    return {k: v for k, v in _flatten_dict(config)}


def _get_interpolated(value: str) -> str:
    if len(value) < 3:
        return value
    if '${' + (name := value[2:-1]) + '}' != value:
        return value
    method, key, default = name.split(':')
    if method not in _methods:
        raise MissingInterpolationMethodException(f'Method {method} is not supported.')
    interpolated = _methods.get(method)(key)
    if interpolated is None:
        return default


def _replace_env(parent: Any, child_key: Any) -> None:
    child = parent[child_key]
    if (t := type(child)) is str:
        parent[child_key] = _get_interpolated(child)
        return
    if t is list or t is dict:
        for v in range(len(child)) if t is list else child.keys():
            _replace_env(child, v)


def _flatten_dict(pyobj, keystring='') -> Tuple[str, Any]:
    if type(pyobj) is dict:
        for k in pyobj:
            yield from _flatten_dict(pyobj[k], str(k))
    else:
        yield keystring, pyobj
