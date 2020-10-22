"""
Get data from the Wikipedi API.
"""

from typing import Any

import click
import requests


def random_page(lang: str) -> Any:
    api_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        with requests.get(api_url) as response:
            response.raise_for_status()  # if bad status, raises exception
            return response.json()  # the API provide its data in json
    except requests.HTTPError:
        raise click.ClickException(
            f'Wikipedia API not reachable OR given language "{lang}" not valid'
        )
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            f'No connection to get "{api_url}" OR given language "{lang}" not valid'
        )
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
