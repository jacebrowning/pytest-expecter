# pylint: disable=unused-variable,expression-not-assigned,redefined-builtin,multiple-statements,bad-continuation,unused-argument

import pytest

from expecter import expect, add_expectation, clear_expectations
from tests.utils import fail_msg


def is_a_potato(thing):
    return thing == 'potato'


def describe_custom_matchers():

    def teardown():
        clear_expectations()

    def they_can_succeed():
        add_expectation(is_a_potato)
        expect('potato').is_a_potato()

    def they_can_fail():
        add_expectation(is_a_potato)
        def _fails():
            expect('not a potato').is_a_potato()
        with pytest.raises(AssertionError):
            _fails()
        assert fail_msg(_fails) == (
            "Expected that 'not a potato' is_a_potato, but it isn't")

    def they_adjust_failure_message_for_expectation_name():
        def can_do_something(thing): return False
        def will_do_something(thing): return False

        for predicate in [can_do_something, will_do_something]:
            add_expectation(predicate)

        assert fail_msg(expect('walrus').can_do_something) == (
            "Expected that 'walrus' can_do_something, but it can't")
        assert fail_msg(expect('walrus').will_do_something) == (
            "Expected that 'walrus' will_do_something, but it won't")

    def they_have_default_failure_message():
        def predicate_with_bad_name(thing): return False
        add_expectation(predicate_with_bad_name)
        assert fail_msg(expect('walrus').predicate_with_bad_name) == (
            "Expected that 'walrus' predicate_with_bad_name, but got False")

    def they_can_be_cleared():
        clear_expectations()
        with pytest.raises(AttributeError):
            expect('potato').is_a_potato

    def they_can_have_postional_arguments():
        def is_a(thing, vegetable):
            return thing == vegetable
        add_expectation(is_a)
        expect('potato').is_a('potato')

    def they_can_have_keyword_arguments():
        def is_a(thing, vegetable):
            return thing == vegetable
        add_expectation(is_a)
        expect('potato').is_a(vegetable='potato')
