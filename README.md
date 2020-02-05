# Overview

A `pytest` plugin based on [garybernhardt/expecter](https://github.com/garybernhardt/expecter) that hides the internal stacktrace.

[![Build Status](https://img.shields.io/travis/jacebrowning/pytest-expecter/develop.svg?label=unix)](https://travis-ci.org/jacebrowning/pytest-expecter)
[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/pytest-expecter/develop.svg)](https://coveralls.io/r/jacebrowning/pytest-expecter)
[![PyPI Version](https://img.shields.io/pypi/v/pytest-expecter.svg)](https://pypi.org/project/pytest-expecter)
[![PyPI License](https://img.shields.io/pypi/l/pytest-expecter.svg)](https://pypi.org/project/pytest-expecter)

# Quick Start

This lets you write tests (optionally using [ropez/pytest-describe](https://github.com/ropez/pytest-describe)) like this:

```python
def describe_foobar():

    def it_can_pass(expect):
        expect(2 + 3) == 5

    def it_can_fail(expect):
        expect(2 + 3) == 6
```

and get output like this:

```text
============================= FAILURES =============================
___________________ describe_foobar.it_can_fail ____________________

    def it_can_fail(expect):
>       expect(2 + 3) == 6
E       AssertionError: Expected 6 but got 5

test_foobar.py:7: AssertionError
================ 1 failed, 1 passed in 2.67 seconds ================
```

# Installation

Install it directly into an activated virtual environment:

```
$ pip install pytest-expecter
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```
$ poetry add pytest-expecter
```

