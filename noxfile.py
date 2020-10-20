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
