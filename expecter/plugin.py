"""
Because this package already takes care of formatting assertions, we want to
disable this behavior in py.test by including this keyword in the docstring:

PYTEST_DONT_REWRITE
"""

import os

import pytest

from . import expect as _expect


def pytest_configure(config):  # pylint: disable=unused-argument
    os.environ['EXPECTER_HIDETRACEBACK'] = "true"


@pytest.fixture
def expect():
    return _expect
