My Hypermodern Python Project
=============================

.. toctree::
    :hidden:
    :maxdepth: 1

    license
    reference

The project following the
`Hypermodern Python <https://cjolowicz.github.io/posts>`_
article series.

The command line interface prints random facts to your console,
using the `Wikipedia API <https://en.wikipedia.org/api/rest_v1/#/>`_.

Installation
------------

To install my Hypermodern Python project,
run this command in your terminal:

.. code-block:: console

    $ pip install my-hypermodern-python

Usage
-----

My Hypermodern Python's usage looks like

.. code-block:: console

    $ my-hypermodern-python [OPTIONS]

.. option:: -l <language>, --lang <language>

    The Wikipedia language edition,
    as identified by its subdomain on

    `wikipedia.org <https://www.wikipedia.org/>`_.
    By default, the English Wikipedia is selected.

.. option:: --version

    Display the version and exit.

.. option:: --help

    Display a short usage message and exit.
