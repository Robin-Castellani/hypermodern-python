"""Get data from the Wikipedia REST API, version 1."""

from dataclasses import dataclass

import click
import desert
import marshmallow
import requests


@dataclass
class Page:
    """Page resource.

    Attributes:
        title: The title of the Wikipedia page.
        extract: A plain text summary.
    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(lang: str = "en") -> Page:
    """Return random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        lang: the Wikipedia language edition.
            By default, the English Wikipedia is used ("en").

    Returns:
        A page resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    Example:
        >>> from my_hypermodern_python import wikipedia
        >>> page = wikipedia.random_page(lang="en")
        >>> bool(page.title)
        True
    """
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
