from A4 import word_counter, word_default
import pytest
example1 = "This example shows how the __missing__() method works behind the scenes in defaultdict. \n It is automatically called when a key is not found, returning the default value instead of raising a KeyError."
example2 = "Relative paths will be interpreted relative to the config file. Multiple paths can be listed (comma separated just like exclude) as needed. If your local plugins have any dependencies, it’s up to you to ensure they are installed in whatever Python environment Flake8 runs in."
example3 = "If your package is installed in the same virtualenv that Flake8 will run from, and your local plugins are part of that package, you’re all set; Flake8 will be able to import your local plugins. "


@pytest.mark.parametrize("example", [
    example1, example2, example3
])
def test_functions_to_each_other(example):
    assert word_counter(example) == word_default(example)


def test_counting():
    assert word_counter('a, a , d a f f') == {'a': 3, 'f': 2, 'd': 1}


def test_default_dict():
    assert word_default('a, a , d a f f') == {'a': 3, 'f': 2, 'd': 1}
