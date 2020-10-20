"""
Test the ``console.py``.
"""

import click.testing
import pytest

from my_hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    # the request is used as a context manager and its json attribute
    #  is accessed to get the data from the API
    mock.return_value.__enter__.return_value.json.return_value = {
        'title': 'Lorem Ipsum',
        'extract': 'Lorem ipsum dolor sit amet',
    }
    return mock


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    # in the terminal output the title is the first line
    output_title = result.output.split('\n')[0]
    assert output_title == 'Lorem Ipsum'


def test_main_prints_extract(runner, mock_requests_get):
    result = runner.invoke(console.main)
    # in the terminal output the extract consists of all lines
    #  but the first one
    output_extract = result.output.split('\n')[1:-1]
    string_extract = ' '.join(output_extract)
    assert string_extract == 'Lorem ipsum dolor sit amet'
