from typing import Any, Tuple

import yaml

from .methods import _configure_methods as methods


def load(config_file: str, flatten: bool = False, override: dict = None):
    """
    :param config_file: Resolvable path of the YAML file containing the config.
    :param (optional) flatten: Boolean value, truthy if you want to flatten the config file.
    :param (optional) override: Map of values to use instead of the config file.
    :param (optional) configure_methods: List of interpolation methods to use.
    """
    with open(config_file, 'r') as inimage:
        config = yaml.safe_load(inimage)
        _interpolate_leafs(config)
        if flatten:
            config = _flatten(config)
        if override:
            config.update(override)
        return config


def _interpolate_leafs(config: dict) -> None:
    for child_key in config.keys():
        _interpolate(config, child_key)


def _get_interpolated(value: str) -> str:
    if len(value) < 3:
        return value
    if '${' + (name := value[2:-1]) + '}' != value:
        return value
    method, key, default = name.split(':', 2)
    interpolated = methods(method)(key)
    if interpolated is None:
        return default
    return interpolated


def _interpolate(parent: Any, child_key: Any) -> None:
    child = parent[child_key]
    if (t := type(child)) is str:
        parent[child_key] = _get_interpolated(child)
        return
    if t is list or t is dict:
        for v in range(len(child)) if t is list else child.keys():
            _interpolate(child, v)


def _flatten(config) -> dict:
    return {k: v for k, v in _flatten_dict(config)}


def _flatten_dict(pyobj, keystring='') -> Tuple[str, Any]:
    if type(pyobj) is dict:
        for k in pyobj:
            yield from _flatten_dict(pyobj[k], str(k))
    else:
        yield keystring, pyobj
