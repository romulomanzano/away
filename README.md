# away
Away.so - Server side logic to consume information from TTN

# Codebase

## Dependencies

- Python 3.7.X

## Keeping Codebase Clean

Please use the python-black pre-commit webhook.

To install just make sure you have pre-commit installed in your local Python 3.7 virtual environment and run the below:

```pre-commit install```

## Python Package Management

We use [pip-tools](https://github.com/jazzband/pip-tools/) (see [rationale](https://nvie.com/posts/pin-your-packages/), [more](https://hynek.me/articles/python-app-deps-2018/)).

This **assumes** you are running a virtualenv.

To add a package:

1. Add package name as a new line into `requirements.in` or, if only required in development, `requirements-dev.in`
2. Run `pip-compile` or `pip-compile requirements-dev.in` depending on which file you updated

To upgrade packages:

```sh
pip-compile --upgrade --output-file requirements-dev.txt requirements-dev.in

pip-compile --upgrade

pip-compile --upgrade-package sentry-sdk
```

You can 'sync' to update your virtual environment to reflect exactly what's in your requirements.

```sh
pip-sync requirements-dev.txt requirements.txt
```
