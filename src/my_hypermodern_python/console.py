"""
The hypermodern Python project
"""

import textwrap

import click
import requests

from . import __version__


API_URL = 'https://en.wikipedia.org/api/rest_v1/page/random/summary'


@click.command()
@click.version_option(version=__version__)
def main():
    """
    Get a random fact from the Wikipedia API

    :return: None
    """

    with requests.get(API_URL) as response:
        response.raise_for_status()  # if bad status, raises exception
        data = response.json()  # the API provide its data in json

    title = data['title']
    extract = data['extract']

    click.secho(title, fg='green')
    click.echo(textwrap.fill(extract))
