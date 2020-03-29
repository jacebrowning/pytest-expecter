# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_can_expect_equality():
        expect(2) == 1 + 1

        def _fails():
            expect(1) == 2

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == 'Expected 2 but got 1'

    def it_can_compare_bytes():
        null = bytes((0,))
        expect(null) == null
        data = bytes(range(9, 32))

        def _fails():
            expect(data) == data + null

        with pytest.raises(AssertionError):
            _fails()

    def it_can_expect_inequality():
        expect(1) != 2

        def _fails():
            expect(1) != 1

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == 'Expected anything except 1 but got it'
