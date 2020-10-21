"""
Nox configuration file.
"""

import nox


# exclude the black session by default
nox.options.sessions = "lint", "test"


@nox.session(python=["3.8", "3.7"])
def test(session):
    # get the positional arguments form the CLI
    # default to --cov
    args = session.posargs or ["--cov"]
    # install dependencies
    # poetry is not part of the environment
    session.run("poetry", "install", external=True)
    # run the tests
    session.run("pytest", *args)


# path to be linted with Flake8
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7"])
def lint(session):
    # get the positional arguments from the CLI or defaults to locations
    args = session.posargs or locations
    # add Flake8 and check if Black would change the code via pip
    session.install("flake8", "flake8-black")
    # run Flake8
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session):
    # get the positional arguments from the CLI or defaults to locations
    args = session.posargs or locations
    # install Black via pip
    session.install("black")
    # run Black
    session.run("black", *args)
