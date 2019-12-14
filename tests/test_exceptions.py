# pylint: disable=unused-variable,expression-not-assigned,redefined-builtin,multiple-statements,bad-continuation

from nose.tools import assert_raises

from expecter import expect
from tests.utils import fail_msg


def describe_expecter_when_expecting_exceptions():

    def it_swallows_expected_exceptions():
        with expect.raises(KeyError):
            raise KeyError

    def it_requires_exceptions_to_be_raised():
        def _expects_raise_but_doesnt_get_it():
            with expect.raises(KeyError):
                pass
        assert_raises(AssertionError, _expects_raise_but_doesnt_get_it)
        assert fail_msg(_expects_raise_but_doesnt_get_it) == (
            'Expected an exception of type KeyError but got none')

    def it_does_not_swallow_exceptions_of_the_wrong_type():
        def _expects_key_error_but_gets_value_error():
            with expect.raises(KeyError):
                raise ValueError
        assert_raises(ValueError, _expects_key_error_but_gets_value_error)

    def it_can_expect_any_exception():
        with expect.raises():
            raise ValueError

    def it_can_expect_failure_messages():
        with expect.raises(ValueError, 'my message'):
            raise ValueError('my message')

    def it_can_require_failure_messages():
        def _fails():
            with expect.raises(ValueError, 'my message'):
                raise ValueError('wrong message')
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected ValueError('my message') but got ValueError('wrong message')")
