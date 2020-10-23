# 🆙 Hypermodern Python
Improving the way I live Python...

This repository follows the tutorial from
[Claudio Jolowicz](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/).

## ❔ What it is...
Get some random facts from the Wikipedia API and print them to the CLI.

To configure and run it, run these commands into the shell
(assuming you have installed at least Python 3.7 and
[Poetry](https://python-poetry.org/docs/)):

```shell script
# checkout the repository (the example is via SSH)
git clone git@github.com:Robin-Castellani/my-hypermodern-python.git
cd my-hypermodern-python

# install dependencies in a separated virtual environment
poetry install

# run it
poetry run my-hypermodern-python
```

## 🛠 Test suite
A small test suite has been implemented with
[Pytest](https://docs.pytest.org/en/stable/).
You can run them
(along with the [Coverage](https://coverage.readthedocs.io/))
with the command

```shell script
poetry run pytest --cov
```

Also, it is possible to run tests in multiple Python environment
(now 3.7 and 3.8) using [Nox](https://nox.thea.codes/en/stable/) with
```shell script
nox
```
Nox runs many sessions (by default `lint`, `safety`, `mypy`, `pytype`,
`test` and `typeguard`); here are the available sessions:
- `lint` to lint the code,
  check whether annotations are present,
  check for security issues,
  check for wrong import order,
  check whether docstrings are present,
  check the correctness of docstring,
  and check whether black would change the code;
- `safety` to check whether third-part packages have security issues;
- `mypy` and `pytype` to statically check types;
- `test` to run the test suite with the coverage;
- `typeguard` to check types at runtime with `pytest`;
- `black` to restyle the code;
- `docs` to build documentation from docstrings using Sphinx;
- `xdoctest` to test the examples in the documentation.

To run a single session, use
```shell script
nox -s <session-name>
```

To speed up the following Nox sessions, reuse the existing virtual envs:
```shell script
nox -rs <session-name>
```

These two custom options are available for `nox`, to be added after `--`:
- `--cov` to get the code coverage of the test suite;
- `-m e2e` or `-m "not e2e"` to perform the test only on or to avoid
  the end to end tests.
