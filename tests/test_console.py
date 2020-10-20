"""
Test the ``console.py``.
"""

import click.testing
import pytest
import requests

from my_hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch('my_hypermodern_python.wikipedia.random_page')


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


def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert 'en.wikipedia.org' in args[0]


def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception('Boom')
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_fails_on_http_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.HTTPError
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_fails_on_connection_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.ConnectionError
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert 'Error' in result.output


def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(console.main, args='--lang=pl')
    mock_wikipedia_random_page.assert_called_with(lang='pl')


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
