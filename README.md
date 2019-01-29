# Overview

A `pytest` plugin for [garybernhardt/expecter](https://github.com/garybernhardt/expecter) that hides the internal stacktrace.

[![Build Status](http://img.shields.io/travis/jacebrowning/pytest-expecter/plugin.svg)](https://travis-ci.org/jacebrowning/pytest-expecter)
[![PyPI Version](http://img.shields.io/pypi/v/pytest-expecter.svg)](https://pypi.python.org/pypi/pytest-expecter)

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

```text
$ pip install pytest-expecter
```
