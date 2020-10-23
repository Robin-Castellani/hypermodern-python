"""Common pytest fixtures."""

from unittest.mock import Mock

from _pytest.config import Config
import pytest
from pytest_mock import MockFixture


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    """It gives a title and an extract to the returned response's JSON."""
    mock = mocker.patch("requests.get")
    # the request is used as a context manager and its json attribute
    #  is accessed to get the data from the API
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


def pytest_configure(config: Config) -> None:
    """Add e2e marker to Pytest."""
    config.addinivalue_line("markers", "e2e: mark as ent-to-end test.")
