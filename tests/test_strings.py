# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_can_expect_startswith():
        expect("fooBar").startswith("foo")

        def _fails():
            expect("fooBar").startswith("Foo")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected 'fooBar' to start with 'Foo' but it didn't"
        )

    def it_can_expect_startswith_ignoring_case():
        expect("fooBar").istartswith("Foo")

        def _fails():
            expect("fooBar").istartswith("qux")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected 'fooBar' to start with 'qux' (ignoring case) but it didn't"
        )

    def it_can_expect_endswith():
        expect("fooBar").endswith("Bar")

        def _fails():
            expect("fooBar").endswith("bar")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected 'fooBar' to end with 'bar' but it didn't")

    def it_can_expect_endswith_ignoring_case():
        expect("fooBar").iendswith("bar")

        def _fails():
            expect("fooBar").iendswith("qux")

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected 'fooBar' to end with 'qux' (ignoring case) but it didn't"
        )
