# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_can_expect_less_than():
        expect(1) < 2

        def _fails():
            expect(1) < 0

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == 'Expected something less than 0 but got 1'

    def it_can_expect_greater_than():
        expect(2) > 1

        def _fails():
            expect(0) > 1

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ('Expected something greater than 1 but got 0')

    def it_can_expect_less_than_or_equal():
        expect(1) <= 1
        expect(1) <= 2

        def _fails():
            expect(2) <= 1

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected something less than or equal to 1 but got 2'
        )

    def it_can_expect_greater_than_or_equal():
        expect(1) >= 1
        expect(2) >= 1

        def _fails():
            expect(1) >= 2

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected something greater than or equal to 2 but got 1'
        )

    def it_can_chain_comparison_expectations():
        # In each of these chains, the first expectation passes and the second
        # fails. This forces the first expectation to return self.
        failing_chains = [
            lambda: 1 == expect(1) != 1,
            lambda: 1 != expect(2) != 2,
            lambda: 1 < expect(2) != 2,
            lambda: 1 > expect(0) != 0,
            lambda: 1 <= expect(1) != 1,
            lambda: 1 >= expect(1) != 1,
        ]
        for chain in failing_chains:
            with pytest.raises(AssertionError):
                chain()
