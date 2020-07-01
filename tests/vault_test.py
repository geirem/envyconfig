import pytest

from src.envyconfig import envyconfig
from src.envyconfig.exceptions.ConfigurationError import ConfigurationError
from src.envyconfig.exceptions.SecretNotFoundError import SecretNotFoundError


@pytest.fixture(name='environment')
def prepare_environment(monkeypatch):
    monkeypatch.setenv("VAULT_ADDR", 'http://localhost:8200/v1')
    monkeypatch.setenv("VAULT_TOKEN", 's.KfdLkD3zeAEXnrRreJxzojDE')
    return monkeypatch


def positive_result_setup():
    data = {
        "request_id": "6b8620df-b47b-e501-3691-9a6ef848095f",
        "lease_id": "",
        "renewable": False,
        "lease_duration": 0,
        "data": {
            "data": {
                "bar_secret": "aosdifjoaidsf",
                "foo_secret": "1235\n2"
            },
            "metadata": {
                "created_time": "2020-07-01T07:41:56.302189Z",
                "deletion_time": "",
                "destroyed": False,
                "version": 2
            }
        },
        "wrap_info": None,
        "warnings": None,
        "auth": None
    }


def test_that_we_handle_missing_token_in_config(environment):
    environment.setenv("VAULT_TOKEN", '')
    with pytest.raises(ConfigurationError):
        envyconfig.load('tests/fixtures/basic_vault.yaml')


def test_that_we_handle_missing_address_in_config(environment):
    environment.setenv("VAULT_ADDR", '')
    with pytest.raises(ConfigurationError):
        envyconfig.load('tests/fixtures/basic_vault.yaml')


def test_with_vault(environment):
    expected = '1235\n2'
    config = envyconfig.load('tests/fixtures/basic_vault.yaml')
    assert config['foo'] == expected


def test_with_older_version_in_vault(environment):
    expected = '1235\n'
    config = envyconfig.load('tests/fixtures/basic_vault.yaml')
    assert config['older_foo'] == expected


def test_with_missing_secret_in_vault(environment):
    with pytest.raises(SecretNotFoundError):
        envyconfig.load('tests/fixtures/missing_vault.yaml')


def test_with_missing_secret_key_in_vault(environment):
    with pytest.raises(SecretNotFoundError):
        envyconfig.load('tests/fixtures/missing_key_vault.yaml')
