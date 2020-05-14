from src.envyconfig import envyconfig
import pytest


def test_basic_gs():
    config = envyconfig.load('fixtures/basic_gs.yaml')
    assert config['bar'] == 'otherwise'
