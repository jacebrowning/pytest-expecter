# pytest-expecter

This is a fork of [garybernhardt/expecter](https://github.com/garybernhardt/expecter) that hides the internal stack trace for `pytest`.

[![Build Status](http://img.shields.io/travis/jacebrowning/pytest-expecter/plugin.svg)](https://travis-ci.org/jacebrowning/pytest-expecter)
[![PyPI Version](http://img.shields.io/pypi/v/pytest-expecter.svg)](https://pypi.python.org/pypi/pytest-expecter)

## Overview

This lets you write tests (using [ropez/pytest-describe](https://github.com/ropez/pytest-describe)) like this:

```python
from expecter import expect


def describe_foobar():

    def it_can_pass():
        expect(2 + 3) == 5

    def it_can_fail():
        expect(2 + 3) == 6
```

and instead of getting output like this:


```sh
=================================== FAILURES ===================================
_________________________ describe_foobar.it_can_fail __________________________

    def it_can_fail():
>       expect(2 + 3) == 6

test_foobar.py:14:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = expect(5), other = 6

    def __eq__(self, other):
        msg = 'Expected %s but got %s' % (repr(other), repr(self._actual))
        if (isinstance(other, basestring) and
                isinstance(self._actual, basestring)):
            msg += normalized_diff(other, self._actual)
        elif len(repr(self._actual)) > 74:
            msg += normalized_diff(pprint.pformat(other),
                                   pprint.pformat(self._actual))
>       assert self._actual == other, msg
E       AssertionError: Expected 6 but got 5

env/lib/python3.5/site-packages/expecter.py:57: AssertionError
====================== 1 failed, 1 passed in 2.67 seconds ======================
```

getting output like this:

```sh
=================================== FAILURES ===================================
_________________________ describe_foobar.it_can_fail __________________________

    def it_can_fail():
>       expect(2 + 3) == 6
E       AssertionError: Expected 6 but got 5

test_foobar.py:14: AssertionError
====================== 1 failed, 1 passed in 2.67 seconds ======================
```

## Installation

```sh
pip install pytest-expecter
```
