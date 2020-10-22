"""
Nox configuration file.
"""

import tempfile

import nox


# exclude the black session by default
nox.options.sessions = "lint", "safety", "mypy", "pytype", "test"


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.7"])
def test(session):
    # get the positional arguments form the CLI
    # default to --cov
    args = session.posargs or ["--cov"]
    # install dependencies
    # poetry is not part of the environment
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    # run the tests
    session.run("pytest", *args)


# path to be linted with Flake8
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7"])
def lint(session):
    # get the positional arguments from the CLI or defaults to locations
    args = session.posargs or locations
    # add Flake8 to lint
    # add check if Black would change the code
    # add check for import statements order
    # add bugbear check
    # all of them via pip
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    # run Flake8
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session):
    # get the positional arguments from the CLI or defaults to locations
    args = session.posargs or locations
    # install Black via pip
    install_with_constraints(session, "black")
    # run Black
    session.run("black", *args)


@nox.session(python="3.8")
def safety(session):
    # open a temporary file
    with tempfile.NamedTemporaryFile() as requirements:
        # convert the poetry .lock file to requirements.txt
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        # install Safety via pip
        install_with_constraints(session, "safety")
        # run Safety
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.7", "3.8"])
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.7", "3.8"])
def pytype(session):
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)
