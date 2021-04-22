import envyconfig


def test_with_supplied_format_parameters():
    formats = {
        'interpolated': 'some_stuff',
    }
    config = envyconfig.load('fixtures/basic_format.yaml', override=formats)
    assert config['foo'] == 'This string will be some_stuff.'
    assert config['bar']['baz1'] == 'This string will also be some_stuff.'

