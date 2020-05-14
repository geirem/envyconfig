from mocks.gs_mock import MockSecrets
from src.envyconfig import envyconfig
import pytest

from src.envyconfig.methods import _gsecrets, _configure_secret_manager
from src.envyconfig import methods


@pytest.fixture(autouse=True)
def inject_method_loader(monkeypatch):
    def mock_configurer():
        return {'gs': lambda s: _gsecrets(MockSecrets(), s)}
    monkeypatch.setattr(methods, '_configure_secret_manager', mock_configurer)


@pytest.mark.skip('basic for now')
def test_basic_gs():
    config = envyconfig.load('fixtures/basic_gs.yaml')
    assert config['bar'] == 'otherwise'
