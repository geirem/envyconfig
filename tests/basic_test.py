from src import envyconfig


def test_basic():
    config = envyconfig.load('tests/fixtures/basic.yaml')
    assert config['foo'] == 'bar'


def test_nested():
    config = envyconfig.load('tests/fixtures/basic_nested.yaml')
    assert config['foo']['bar'] == 'baz'


def test_flattened():
    config = envyconfig.load('tests/fixtures/basic_nested.yaml', flatten=True)
    assert config['bar'] == 'baz'


def test_empty_value():
    config = envyconfig.load('tests/fixtures/basic.yaml')
    assert config['baz'] == ''
