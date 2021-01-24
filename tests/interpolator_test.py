from src import envyconfig


def test_multiple_colons():
    config = envyconfig.load('tests/fixtures/complex.yaml')
    assert config['foo'] == 'default:with:'


def test_that_we_duck_type_basic_defaults() -> None:
    config = envyconfig.load('tests/fixtures/basic_env.yaml')
    typed = config['bar']
    assert type(typed['baz1']) is bool
    assert not typed['baz1']
    assert type(typed['baz2']) is bool
    assert typed['baz2']
    assert type(typed['baz3']) is int
    assert typed['baz3'] == 1232
    assert type(typed['baz4']) is float
    assert typed['baz4'] == 1232.2
    assert type(typed['baz5']) is str
    assert typed['baz5'] == 'abcd'


def test_that_we_allow_missing_defaults() -> None:
    config = envyconfig.load('tests/fixtures/basic_env.yaml')
    typed = config['bar']
    assert typed['baz6'] is None
