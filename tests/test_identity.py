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
        assert fail_msg(_fails) == ("Expected condition to be True, but it was False")

    def it_can_expect_identity_with_false():
        expect(1 > 2).is_(False)

        def _fails():
            expect(1 < 2).is_(False)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected condition to be False, but it was True")

    def it_can_expect_identity_with_none():
        data = {'a': 1}

        expect(data.get('b')).is_(None)

        def _fails():
            expect(data.get('a')).is_(None)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected value to be None, but it was 1")

    def it_can_expect_nonidentity_with_true():
        expect(1 > 2).is_not(True)

        def _fails():
            expect(1 < 2).is_not(True)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected condition to not be True, but it was")

    def it_can_expect_nonidentity_with_false():
        expect(1 < 2).is_not(False)

        def _fails():
            expect(1 > 2).is_not(False)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected condition to not be False, but it was")

    def it_can_expect_nonidentity_with_None():
        data = {'a': 1}

        expect(data.get('a')).is_not(None)

        def _fails():
            expect(data.get('b')).is_not(None)

        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == ("Expected value to not be None, but it was")
