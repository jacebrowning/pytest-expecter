# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_can_expect_containment():
        expect([1]).contains(1)

        def _fails():
            expect([2]).contains(1)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected [2] to contain 1 but it didn't")

    def it_can_expect_containment_ignoring_case():
        expect("fooBar").icontains("FooBAR")

        def _fails():
            expect("fooBar").icontains("Qux")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected 'fooBar' to contain 'Qux' (ignoring case) but it didn't"
        )

    def it_can_expect_non_containment():
        expect([1]).does_not_contain(0)

        def _fails():
            expect([1]).does_not_contain(1)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected [1] not to contain 1 but it did")

    def it_can_expect_exclusion():
        expect([1]).excludes(0)

        def _fails():
            expect([1]).excludes(1)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected [1] to exclude 1 but it didn't")

    def it_can_expect_exclusion_ignoring_case():
        expect([1]).iexcludes(0)

        def _fails():
            expect([1]).iexcludes(1)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected [1] to exclude 1 (ignoring case) but it didn't"
        )

    def it_optimizes_containment_message_for_multiline_strings():
        expect("<p>\nHello, world!\n</p>\n").contains("Hello, world!")

        def _fails():
            expect("<p>\nHello, world!\n</p>\n").contains("Foobar")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected to contain 'Foobar' but didn't"
        )

    def it_optimizes_non_containment_message_for_multiline_strings():
        expect("<p>\nHello, world!\n</p>\n").does_not_contain("Foobar")

        def _fails():
            expect("<p>\nHello, world!\n</p>\n").does_not_contain("Hello")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected not to contain 'Hello' but did"
        )

    def it_optimizes_exclusion_message_for_multiline_strings():
        expect("<p>\nHello, world!\n</p>\n").excludes("Foobar")

        def _fails():
            expect("<p>\nHello, world!\n</p>\n").excludes("Hello")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected to exclude 'Hello' but didn't"
        )
