# pylint: disable=unused-variable,expression-not-assigned

import pytest

from expecter import expect
from tests.utils import fail_msg


def describe_expect():
    def it_can_expect_identity_with_true():
        expect(1 < 2).is_(True)

        def _fails():
            expect(1 > 2).is_(True)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected value to be True, but it wasn't")

    def it_can_expect_identity_with_false():
        expect(1 > 2).is_(False)

        def _fails():
            expect(1 < 2).is_(False)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected value to be False, but it wasn't")

    def it_can_expect_identity_with_none():
        data = {'a': 1}

        expect(data.get('b')).is_(None)

        def _fails():
            expect(data.get('a')).is_(None)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected value to be None, but it wasn't")
