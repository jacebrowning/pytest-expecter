# pylint: disable=unused-variable,expression-not-assigned

import sys
from collections import OrderedDict

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_shows_diff_when_strings_differ():
        def _fails():
            expect('foo\nbar') == 'foo\nbaz'

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected 'foo\\nbaz' but got 'foo\\nbar'\n"
            "Diff:\n"
            "@@ -1,2 +1,2 @@\n"
            " foo\n"
            "-baz\n"
            "+bar"
        ), fail_msg(_fails)

    def it_shows_diff_for_large_reprs():
        sequence = list(range(1000, 1050))
        big_list = sequence[:20] + [1019] + sequence[20:]

        def _fails():
            expect(big_list) == sequence

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected {0} but got {1}\n"
            "Diff:\n"
            "@@ -17,6 +17,7 @@\n"
            "  1016,\n"
            "  1017,\n"
            "  1018,\n"
            "+ 1019,\n"
            "  1019,\n"
            "  1020,\n"
            "  1021,"
        ).format(repr(sequence), repr(big_list)), fail_msg(_fails)

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="Only valid on Python 3.6+")
    def it_shows_optimized_diff_for_ordereddict_on_python36():
        actual = [OrderedDict(a=1, b=2, c=3, d=4, e=5, f=6)]
        expected = [dict(a=1, b=22, c=3, d=4, f=6, g=7)]
        expect.MIN_DIFF_SIZE = 10

        def _fails():
            expect(actual) == expected

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected "
            "[{'a': 1, 'b': 22, 'c': 3, 'd': 4, 'f': 6, 'g': 7}] but got "
            "[{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}]\n"
            "Diff:\n"
            "@@ -1 +1 @@\n"
            "-[{'a': 1, 'b': 22, 'c': 3, 'd': 4, 'f': 6, 'g': 7}]\n"
            "+[{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}]"
        ), fail_msg(_fails)

    def it_supports_ignoring_values_with_anything():
        def _fails():
            expect({'foo': 2, 'bar': None}) == {'foo': 1, 'bar': expect.anything}

        with pytest.raises(AssertionError):
            _fails()
        assert "'bar': <anything>" in fail_msg(_fails), fail_msg(_fails)
