# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_can_expect_instance():
        expect(1).isinstance(int)

        def _fails():
            expect(1).isinstance(str)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected an instance of str but got an instance of int'
        )

    def it_can_expect_instance_for_multiple_types():
        expect('str').isinstance((str, bytes))

        def _fails():
            expect('str').isinstance((int, tuple))

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            'Expected an instance of int or tuple but got an instance of str'
        )
