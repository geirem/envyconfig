import pytest

from mocks.vault_broker_mock import VaultBrokerMock
import envyconfig
from envyconfig import methods
from envyconfig.exceptions.ConfigurationError import ConfigurationError
from envyconfig.exceptions.SecretNotFoundError import SecretNotFoundError


@pytest.fixture(name='broker')
def create_broker(environment):
    broker = VaultBrokerMock(environment)

    def mock_configurer():
        return {'vault': lambda s: broker(s)}
    methods._methods = {}
    environment.setattr(methods, '_configure_hashicorp_vault', mock_configurer)
    return broker


@pytest.fixture(name='environment', autouse=True)
def prepare_environment(monkeypatch):
    monkeypatch.setenv("VAULT_ADDR", 'http://localhost:8200/v1')
    monkeypatch.setenv("VAULT_TOKEN", 's.KfdLkD3zeAEXnrRreJxzojDE')
    return monkeypatch


def test_that_we_handle_missing_token_in_config(environment):
    environment.setenv("VAULT_TOKEN", '')
    with pytest.raises(ConfigurationError):
        envyconfig.load('fixtures/basic_vault.yaml')


def test_that_we_handle_missing_address_in_config(environment):
    environment.setenv("VAULT_ADDR", '')
    with pytest.raises(ConfigurationError):
        envyconfig.load('fixtures/basic_vault.yaml')


def test_with_vault(broker):
    expected = '1235\n2'
    broker.setup(
        {
            "data": {
                "foo_secret": expected
            },
            'version': 2,
            'status_code': 200,
        }
    )
    config = envyconfig.load('fixtures/basic_vault.yaml')
    assert config['foo'] == expected


def test_with_older_version_in_vault(broker):
    expected = '1235\n'
    broker.setup(
        {
            "data": {
                "foo_secret": expected
            },
            'version': 1,
            'status_code': 200,
        }
    )
    config = envyconfig.load('fixtures/basic_vault.yaml')
    assert config['older_foo'] == expected


def test_with_missing_secret_in_vault(broker):
    broker.setup(
        {
            "data": {},
            'status_code': 404,
        }
    )
    with pytest.raises(SecretNotFoundError):
        envyconfig.load('fixtures/missing_vault.yaml')


def test_with_missing_secret_key_in_vault(broker):
    broker.setup(
        {
            "data": {},
            'status_code': 200,
        }
    )
    with pytest.raises(SecretNotFoundError):
        envyconfig.load('fixtures/missing_key_vault.yaml')
