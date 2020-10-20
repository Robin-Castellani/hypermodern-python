"""
Common pytest fixtures.
"""

import pytest


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


def pytest_configure(config):
    config.addinivalue_line('markers', "e2e: mark as ent-to-end test.")
