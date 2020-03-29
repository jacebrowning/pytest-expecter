# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_shows_diff_when_strings_differ():
        value = 'ueber\ngeek'
        fixture = 'über\ngeek'
        assert isinstance(value, str), "value is a " + repr(type(value))
        assert isinstance(fixture, str), "fixture is a " + repr(type(fixture))

        def _fails():
            expect(value) == fixture

        with pytest.raises(AssertionError):
            _fails()
        msg = (
            "Expected 'über\\ngeek' but got 'ueber\\ngeek'\n"
            "Diff:\n"
            "@@ -1,2 +1,2 @@\n"
            "-über\n"
            "+ueber\n"
            " geek"
        )
        # Normalize real msg for differences in py2 and py3
        real = fail_msg(_fails).replace("u'", "'").replace('\\xfc', '\xfc')
        assert real == msg, '\n' + repr(real) + '\n' + repr(msg)
