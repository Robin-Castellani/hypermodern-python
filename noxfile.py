"""
Nox configuration file.
"""

import nox


@nox.session(python=['3.8', '3.7'])
def test(session):
    # get the positional arguments form the CLI
    # default to --cov
    args = session.posargs or ['--cov']
    # install dependencies
    # poetry is not part of the environment
    session.run('poetry', 'install', external=True)
    # run the tests
    session.run('pytest', *args)


# path to be linted with Flake8
locations = "src", "tests", "noxfile.py"


@nox.session(python=['3.8', '3.7'])
def lint(session):
    # get the positional arguments from the CLI or defaults to locations
    args = session.posargs or locations
    # add Flake8 via pip
    session.install("flake8")
    # run Flake8
    session.run("flake8", *args)
