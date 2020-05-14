from typing import Any, Tuple

import yaml

from .exceptions.UnsupportedInterpolationError import UnsupportedInterpolationError
from .methods import _configure_methods


def load(config_file: str, flatten: bool = False, override: dict = None, configure_methods=True):
    """
    :param config_file: Resolvable path of the YAML file containing the config.
    :param (optional) flat_map: Boolean value, truthy if you want to flatten the config file.
    :param (optional) override: Map of values to use instead of the config file.
    """
    with open(config_file, 'r') as inimage:
        config = yaml.safe_load(inimage)
        _interpolate_leafs(config, _configure_methods(configure_methods))
        if flatten:
            config = _flatten(config)
        if override:
            config.update(override)
        return config


def _interpolate_leafs(config: dict, methods) -> None:
    for child_key in config.keys():
        _interpolate(config, child_key, methods)


def _get_interpolated(value: str, methods) -> str:
    if len(value) < 3:
        return value
    if '${' + (name := value[2:-1]) + '}' != value:
        return value
    method, key, default = name.split(':')
    if method not in methods:
        raise UnsupportedInterpolationError(f'Method {method} is not supported.')
    interpolated = methods.get(method)(key)
    if interpolated is None:
        return default


def _interpolate(parent: Any, child_key: Any, _methods) -> None:
    child = parent[child_key]
    if (t := type(child)) is str:
        parent[child_key] = _get_interpolated(child, _methods)
        return
    if t is list or t is dict:
        for v in range(len(child)) if t is list else child.keys():
            _interpolate(child, v, _methods)


def _flatten(config) -> dict:
    return {k: v for k, v in _flatten_dict(config)}


def _flatten_dict(pyobj, keystring='') -> Tuple[str, Any]:
    if type(pyobj) is dict:
        for k in pyobj:
            yield from _flatten_dict(pyobj[k], str(k))
    else:
        yield keystring, pyobj
