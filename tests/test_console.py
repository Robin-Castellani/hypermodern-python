"""
Test the ``console.py``.
"""

from unittest.mock import Mock

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from my_hypermodern_python import console


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    return mocker.patch("my_hypermodern_python.wikipedia.random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    # in the terminal output the title is the first line
    output_title = result.output.split("\n")[0]
    assert output_title == "Lorem Ipsum"


def test_main_prints_extract(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    # in the terminal output the extract consists of all lines
    #  but the first one
    output_extract = result.output.split("\n")[1:-1]
    string_extract = " ".join(output_extract)
    assert string_extract == "Lorem ipsum dolor sit amet"


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_fails_on_http_error(runner: CliRunner, mock_requests_get: Mock) -> None:
    mock_requests_get.side_effect = requests.HTTPError
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_fails_on_connection_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.exceptions.ConnectionError
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    runner.invoke(console.main, args="--lang=pl")
    mock_wikipedia_random_page.assert_called_with(lang="pl")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
