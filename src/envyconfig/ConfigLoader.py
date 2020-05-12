import os
from typing import Any, Tuple

import yaml


class ConfigLoader:

    def __init__(self, config_file: str, flat_map: bool = False, override: dict = None):
        """
        :param config_file: Resolvable path of the YAML file containing the config.
        :param (optional) flat_map: Boolean value, truthy if you want to flatten the config file.
        :param (optional) override: Map of values to use instead of the config file.
        """
        self._config_file = config_file
        self._flat_map = flat_map
        self._args = {} if override is None else override

    def load(self) -> dict:
        with open(self._config_file) as inimage:
            config = yaml.safe_load(inimage)
        for child_key in config.keys():
            self._replace_env(config, child_key)
        if self._flat_map:
            config = {k: v for k, v in self._flatten_dict(config)}
        for k in config:
            if k in self._args:
                config[k] = self._args[k]
        return config

    def _replace_env(self, parent: Any, child_key: Any) -> None:
        child = parent[child_key]
        if type(child) is str:
            if '${' + child[2:-1] + '}' == child:
                parent[child_key] = os.environ[child[2:-1]]
        elif type(child) is list:
            for i in range(len(child)):
                self._replace_env(child, i)
        elif type(child) is dict:
            for v in child.keys():
                self._replace_env(child, v)

    def _flatten_dict(self, pyobj, keystring='') -> Tuple[str, Any]:
        if type(pyobj) is dict:
            for k in pyobj:
                yield from self._flatten_dict(pyobj[k], str(k))
        else:
            yield keystring, pyobj
