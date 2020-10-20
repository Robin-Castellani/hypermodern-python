"""
The hypermodern Python project
"""

import textwrap

import click
import requests

from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.option('--lang', default='en', help='Which language do you want?')
def main(lang):
    """
    Get a random fact from the Wikipedia API
    """
    api_url = 'https://en.wikipedia.org/api/rest_v1/page/random/summary'

    api_url = api_url.replace('en', lang, 1)

    try:
        with requests.get(api_url) as response:
            response.raise_for_status()  # if bad status, raises exception
            data = response.json()  # the API provide its data in json
    except requests.HTTPError:
        raise click.ClickException(
            f'Wikipedia API not reachable OR given language "{lang}" not valid'
        )
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            f'Given language "{lang}" not valid'
        )

    title = data['title']
    extract = data['extract']

    click.secho(title, fg='green')
    click.echo(textwrap.fill(extract))
