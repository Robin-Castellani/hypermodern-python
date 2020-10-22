"""
The hypermodern Python project.

Print the a random fact using the Wikipedia API.
"""

# import locale
import textwrap

import click

from . import __version__, wikipedia


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--lang",
    "-l",
    default="en",  # locale.getdefaultlocale()[0].split("_")[0],
    show_default=True,
    help="Which language do you want?",
    metavar="LANG",
)
def main(lang: str) -> None:
    """
    Get a random fact from the Wikipedia API
    """
    # import pdb;pdb.set_trace()
    page = wikipedia.random_page(lang=lang)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
