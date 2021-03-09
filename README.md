[![Build Status](https://travis-ci.com/antoniouaa/verbose-octo-guide.svg?branch=master)](https://travis-ci.com/antoniouaa/verbose-octo-guide) [![Coverage Status](https://coveralls.io/repos/github/antoniouaa/verbose-octo-guide/badge.svg?branch=master)](https://coveralls.io/github/antoniouaa/verbose-octo-guide?branch=master)

A small Flask server for the simple processing of genome sequences

### Run locally

You'll need to install [poetry](https://python-poetry.org/) first.

First clone the repository, move inside the new directory, set the proper env variables and run the poetry command.

```sh
git clone https://github/antoniouaa/verbose-octo-guide.git
cd verbose-octo-guide
```

For linux:

```sh
export FLASK_APP="run.py"
```

For Powershell:

```sh
$env:FLASK_APP="run.py"
```

Run with poetry run:

```sh
poetry run flask run
```

### To run the tests

```sh
poetry run pytest --cov="sequencer"  tests/
```
