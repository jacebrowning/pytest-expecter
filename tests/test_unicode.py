# -*- coding: utf-8 -*-
# pylint: disable=unused-variable,expression-not-assigned,redefined-builtin,multiple-statements,bad-continuation


from __future__ import unicode_literals

import pytest

from expecter import expect
from tests.utils import fail_msg

try:
    import builtins as __builtins__
except ImportError:
    import __builtin__ as __builtins__

unicode = getattr(__builtins__, 'unicode', str)


def describe_expecter():

    def it_shows_diff_when_unicode_strings_differ():
        value = 'ueber\ngeek'
        fixture = 'über\ngeek'
        assert isinstance(value, unicode), "value is a " + repr(type(value))
        assert isinstance(fixture, unicode), "fixture is a " + repr(type(fixture))
        def _fails():
            expect(value) == fixture
        with pytest.raises(AssertionError):
            _fails()
        msg = ("Expected 'über\\ngeek' but got 'ueber\\ngeek'\n"
               "Diff:\n"
               "@@ -1,2 +1,2 @@\n"
               "-über\n"
               "+ueber\n"
               " geek"
               )
        # Normalize real msg for differences in py2 and py3
        real = fail_msg(_fails).replace("u'", "'").replace('\\xfc', '\xfc')
        assert real == msg, '\n' + repr(real) + '\n' + repr(msg)
