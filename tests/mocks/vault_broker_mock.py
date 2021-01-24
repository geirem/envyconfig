import json
import os
from collections import namedtuple

import requests

Response = namedtuple('Response', ['status_code', 'text', 'json'])


class MockRequest:

    def __init__(self, config: dict):
        self._data = config['data']
        self._response = Response(config['status_code'], json.dumps(config['data']), self.json)

    def get(self, *args, **kwargs):
        return self._response

    def json(self):
        return self._data


class VaultBrokerMock(VaultBroker):

    def __init__(self, monkeypatch):
        super(VaultBrokerMock, self).__init__(os.environ['VAULT_ADDR'], os.environ['VAULT_TOKEN'])
        self._monkeypatch = monkeypatch

    def setup(self, config: dict) -> None:
        data = {
            "request_id": "6b8620df-b47b-e501-3691-9a6ef848095f",
            "lease_id": "",
            "renewable": False,
            "lease_duration": 0,
            "data": {
                "data": config['data'],
                "metadata": {
                    "created_time": "2020-07-01T07:41:56.302189Z",
                    "deletion_time": "",
                    "destroyed": False,
                    "version": config['version'] if 'version' in config else 1,
                }
            },
            "wrap_info": None,
            "warnings": None,
            "auth": None
        }
        config['data'] = data
        requests_mock = MockRequest(config)
        self._monkeypatch.setattr(requests, 'get', requests_mock.get)
