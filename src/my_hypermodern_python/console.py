"""
The hypermodern Python project.

Print the a random fact using the Wikipedia API.
"""

import textwrap
import locale

import click
import requests

from . import __version__, wikipedia


@click.command()
@click.version_option(version=__version__)
@click.option(
    '--lang', default=locale.getdefaultlocale()[0].split('_')[0],
    help='Which language do you want?'
)
def main(lang):
    """
    Get a random fact from the Wikipedia API
    """
    data = wikipedia.random_page(lang)

    title = data['title']
    extract = data['extract']

    click.secho(title, fg='green')
    click.echo(textwrap.fill(extract))
