# pylint: disable=unused-variable,expression-not-assigned,redefined-builtin,multiple-statements,bad-continuation

from __future__ import with_statement

import sys
from collections import OrderedDict

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expecter():

    def it_expects_equals():
        expect(2) == 1 + 1
        def _fails(): expect(1) == 2
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == 'Expected 2 but got 1'

    def it_shows_diff_when_strings_differ():
        def _fails(): expect('foo\nbar') == 'foo\nbaz'
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected 'foo\\nbaz' but got 'foo\\nbar'\n"
               "Diff:\n"
               "@@ -1,2 +1,2 @@\n"
               " foo\n"
               "-baz\n"
               "+bar"
               ), fail_msg(_fails)

    def it_shows_diff_for_large_reprs():
        sequence = list(range(1000, 1050))
        big_list = sequence[:20] + [1019] + sequence[20:]
        def _fails(): expect(big_list) == sequence
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected {0} but got {1}\n"
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

    @pytest.mark.skipif(sys.version < '3.6',
                        reason="Only valid on Python 3.6+")
    def it_shows_optimized_diff_for_ordereddict_on_python36():
        actual = [OrderedDict(a=1, b=2, c=3, d=4, e=5, f=6)]
        expected = [dict(a=1, b=22, c=3, d=4, f=6, g=7)]
        expect.MIN_DIFF_SIZE = 10
        def _fails(): expect(actual) == expected
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

    def it_can_compare_bytes():
        null = bytes((0,))
        expect(null) == null
        data = bytes(range(9, 32))
        def _fails():
            expect(data) == data + null
        with pytest.raises(AssertionError):
            _fails()

    def it_expects_not_equals():
        expect(1) != 2
        def _fails(): expect(1) != 1
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == 'Expected anything except 1 but got it'

    def it_expects_less_than():
        expect(1) < 2
        def _fails(): expect(1) < 0
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == 'Expected something less than 0 but got 1'

    def it_expects_greater_than():
        expect(2) > 1
        def _fails(): expect(0) > 1
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected something greater than 1 but got 0')

    def it_expects_less_than_or_equal():
        expect(1) <= 1
        expect(1) <= 2
        def _fails(): expect(2) <= 1
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected something less than or equal to 1 but got 2')

    def it_expects_greater_than_or_equal():
        expect(1) >= 1
        expect(2) >= 1
        def _fails(): expect(1) >= 2
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected something greater than or equal to 2 but got 1')

    def it_can_chain_comparison_expectations():
        # In each of these chains, the first expectation passes and the second
        # fails. This forces the first expectation to return self.
        failing_chains = [lambda: 1 == expect(1) != 1,
                          lambda: 1 != expect(2) != 2,
                          lambda: 1 < expect(2) != 2,
                          lambda: 1 > expect(0) != 0,
                          lambda: 1 <= expect(1) != 1,
                          lambda: 1 >= expect(1) != 1]
        for chain in failing_chains:
            with pytest.raises(AssertionError):
                chain()

    def it_can_expect_instance():
        expect(1).isinstance(int)
        def _fails():
            expect(1).isinstance(str)
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected an instance of str but got an instance of int')

    def it_can_expect_instance_for_multiple_types():
        expect('str').isinstance((str, bytes))
        def _fails():
            expect('str').isinstance((int, tuple))
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected an instance of int or tuple but got an instance of str')

    def it_can_expect_containment():
        expect([1]).contains(1)
        def _fails():
            expect([2]).contains(1)
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected [2] to contain 1 but it didn't")

    def it_can_expect_containment_ignoring_case():
        expect("fooBar").icontains("FooBAR")
        def _fails():
            expect("fooBar").icontains("Qux")
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected 'fooBar' to contain 'Qux' (ignoring case) but it didn't")

    def it_can_expect_non_containment():
        expect([1]).does_not_contain(0)
        def _fails():
            expect([1]).does_not_contain(1)
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected [1] not to contain 1 but it did")

    def it_can_expect_exclusion():
        expect([1]).excludes(0)
        def _fails():
            expect([1]).excludes(1)
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected [1] to exclude 1 but it didn't")

    def it_can_expect_exclusion_ignoring_case():
        expect([1]).iexcludes(0)
        def _fails():
            expect([1]).iexcludes(1)
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected [1] to exclude 1 (ignoring case) but it didn't")

    def it_optimizes_containment_message_for_multiline_strings():
        expect("<p>\nHello, world!\n</p>\n").contains("Hello, world!")
        def _fails():
            expect("<p>\nHello, world!\n</p>\n").contains("Foobar")
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected to contain 'Foobar' but didn't")

    def it_optimizes_non_containment_message_for_multiline_strings():
        expect("<p>\nHello, world!\n</p>\n").does_not_contain("Foobar")
        def _fails():
            expect("<p>\nHello, world!\n</p>\n").does_not_contain("Hello")
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected not to contain 'Hello' but did")

    def it_optimizes_exclusion_message_for_multiline_strings():
        expect("<p>\nHello, world!\n</p>\n").excludes("Foobar")
        def _fails():
            expect("<p>\nHello, world!\n</p>\n").excludes("Hello")
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected to exclude 'Hello' but didn't")
