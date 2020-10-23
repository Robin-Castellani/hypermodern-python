"""Nox configuration file."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session


# exclude the black session by default
nox.options.sessions = "lint", "safety", "mypy", "pytype", "test", "typeguard"
# path to be linted with Flake8
locations = "src", "tests", "noxfile.py", "docs/conf.py"
# package to be analysed with Typeguard
package = "my_hypermodern_python"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by poetry's lock file."""
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
def test(session: Session) -> None:
    """Run the test suite."""
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


@nox.session(python=["3.8", "3.7"])
def lint(session: Session) -> None:
    """Lint using flake8."""
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
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    # run Flake8
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    # get the positional arguments from the CLI or defaults to locations
    args = session.posargs or locations
    # install Black via pip
    install_with_constraints(session, "black")
    # run Black
    session.run("black", *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    install_with_constraints(session, "sphinx")
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
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
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.7", "3.8"])
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.8", "3.7"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    # exclude ent-to-end tests by default
    args = session.posargs or ["-m", "not e2e"]
    # install package dependencies
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    # run typeguard as a pytest plugin
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=["3.8", "3.7"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    # set "all" as a default argument
    args = session.posargs or ["all"]
    # install al non dev dependencies
    session.run("poetry", "install", "--no-dev", external=True)
    # install xdoctest
    install_with_constraints(session, "xdoctest")
    # run xdoctest
    session.run("python", "-m", "xdoctest", package, *args)
