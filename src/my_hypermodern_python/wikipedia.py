"""
Get data from the Wikipedi API.
"""

from dataclasses import dataclass

import click
import desert
import marshmallow
import requests


@dataclass
class Page:
    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(lang: str = "en") -> Page:
    api_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        with requests.get(api_url) as response:
            response.raise_for_status()  # if bad status, raises exception
            data = response.json()  # the API provide its data in json
            return schema.load(data)
    except requests.HTTPError:
        raise click.ClickException(
            f'Wikipedia API not reachable OR given language "{lang}" not valid'
        )
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            f'No connection to get "{api_url}" OR given language "{lang}" not valid'
        )
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
