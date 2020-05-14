from mocks.gs_mock import MockSecrets
from src.envyconfig import envyconfig
import pytest

from src.envyconfig.methods import _gsecrets, _configure_secret_manager
from src.envyconfig import methods


def test_basic():
    config = envyconfig.load('fixtures/basic.yaml', configure_methods=False)
    assert config['foo'] == 'bar'


def test_nested():
    config = envyconfig.load('fixtures/basic_nested.yaml', configure_methods=False)
    assert config['foo']['bar'] == 'baz'


def test_flattened():
    config = envyconfig.load('fixtures/basic_nested.yaml', configure_methods=False, flatten=True)
    assert config['bar'] == 'baz'
