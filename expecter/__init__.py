"""
Because this package already takes care of formatting assertions, we want to
disable this behavior in py.test by including this keyword in the docstring:

PYTEST_DONT_REWRITE
"""

import difflib
import os
import pprint
import sys
from collections import OrderedDict

import pytest
from pkg_resources import DistributionNotFound, get_distribution


try:
    __version__ = get_distribution('pytest-expecter').version
except DistributionNotFound:
    __version__ = '(local)'


__all__ = ['expect']


class Anything:
    """Placeholder value to ignore uninteresting response data."""

    def __repr__(self):
        return '<anything>'

    def __eq__(self, other):
        return True


class expect:
    """
    All assertions are written using :class:`expect`. Usually, it's applied to
    the value you're making an assertion about:

        >>> expect(5) > 4
        expect(5)
        >>> expect(4) > 4
        Traceback (most recent call last):
        ...
        AssertionError: Expected something greater than 4 but got 4

    This works for comparisons as you'd expect:

        ==, !=, <, >, <=, >=

    Note that expect() *always* goes around the actual value: the value you're
    making an assertion about.

    There are other, non-binary expectations available. They're documented
    below.
    """

    MIN_DIFF_SIZE = 74

    anything = Anything()

    def __init__(self, actual):
        self._actual = normalize(actual)

    def __getattr__(self, name):
        is_custom_expectation = name in _custom_expectations
        if is_custom_expectation:
            predicate = _custom_expectations[name]
            return _CustomExpectation(predicate, self._actual)
        return getattr(super(), name)

    def __eq__(self, other):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        msg = 'Expected %s but got %s' % (repr(other), repr(self._actual))
        if isinstance(other, str) and isinstance(self._actual, str):
            msg += normalized_diff(other, self._actual)
        elif len(repr(self._actual)) > self.MIN_DIFF_SIZE:
            msg += normalized_diff(pprint.pformat(other), pprint.pformat(self._actual))
        assert self._actual == other, msg
        return self

    def __ne__(self, other):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        assert self._actual != other, 'Expected anything except %s but got it' % repr(
            self._actual
        )
        return self

    def __lt__(self, other):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        assert self._actual < other, 'Expected something less than %s but got %s' % (
            repr(other),
            repr(self._actual),
        )
        return self

    def __gt__(self, other):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        assert self._actual > other, 'Expected something greater than %s but got %s' % (
            repr(other),
            repr(self._actual),
        )
        return self

    def __le__(self, other):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        assert self._actual <= other, (
            'Expected something less than or equal to %s but got %s'
            % (repr(other), repr(self._actual))
        )
        return self

    def __ge__(self, other):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        assert self._actual >= other, (
            'Expected something greater than or equal to %s but got %s'
            % (repr(other), repr(self._actual))
        )
        return self

    def __repr__(self):
        return 'expect(%s)' % repr(self._actual)

    def is_(self, other):
        """Ensure that ``other`` is identical to the actual value."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        label = 'condition' if isinstance(self._actual, bool) else 'value'
        assert self._actual is other, "Expected %s to be %s, but it was %s" % (
            label,
            repr(other),
            repr(self._actual),
        )
        return self

    def is_not(self, other):
        """Ensure that ``other`` is not identical to the actual value."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        label = 'condition' if isinstance(self._actual, bool) else 'value'
        assert self._actual is not other, "Expected %s to not be %s, but it was" % (
            label,
            repr(other),
        )
        return self

    def isinstance(self, expected_cls):
        """Ensure the actual value is of type ``expected_cls``.

        This is similar to ``assert isinstance(actual, MyClass)``.
        """
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        if isinstance(expected_cls, tuple):
            cls_name = [c.__name__ for c in expected_cls]
            cls_name = ' or '.join(cls_name)  # type: ignore
        else:
            cls_name = expected_cls.__name__
        assert isinstance(self._actual, expected_cls), (
            'Expected an instance of %s but got an instance of %s'
            % (cls_name, self._actual.__class__.__name__)
        )

    def contains(self, other):
        """Ensure that ``other`` is in the actual value.

        This is similar to ``assert other in actual``.
        """
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = "Given text:\n\n%s\n\nExpected to contain %s but didn't" % (
                self._actual.strip(),
                repr(other),
            )
        else:
            msg = "Expected %s to contain %s but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert other in self._actual, msg

    def icontains(self, other):
        """Same as ``contains` but ignoring case."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = (
                "Given text:\n\n%s\n\nExpected to contain %s (ignoring case) but didn't"
                % (self._actual.strip(), repr(other))
            )
        else:
            msg = "Expected %s to contain %s (ignoring case) but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        expected = other.lower() if isinstance(other, str) else other
        actual = self._actual.lower() if isinstance(self._actual, str) else self._actual

        assert expected in actual, msg

    def includes(self, other):
        """Same as ``contains`` but with alternate phrasing."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = "Given text:\n\n%s\n\nExpected to include %s but didn't" % (
                self._actual.strip(),
                repr(other),
            )
        else:
            msg = "Expected %s to include %s but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert other in self._actual, msg

    def does_not_contain(self, other):
        """Opposite of ``contains``."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = "Given text:\n\n%s\n\nExpected not to contain %s but did" % (
                self._actual.strip(),
                repr(other),
            )
        else:
            msg = "Expected %s not to contain %s but it did" % (
                repr(self._actual),
                repr(other),
            )

        assert other not in self._actual, msg

    def excludes(self, other):
        """Opposite of ``contains`` with alternate phrasing."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = "Given text:\n\n%s\n\nExpected to exclude %s but didn't" % (
                self._actual.strip(),
                repr(other),
            )
        else:
            msg = "Expected %s to exclude %s but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert other not in self._actual, msg

    def iexcludes(self, other):
        """Same as ``excludes`` but ignoring case."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = (
                "Given text:\n\n%s\n\nExpected to exclude %s (ignoring case) but didn't"
                % (self._actual.strip(), repr(other))
            )
        else:
            msg = "Expected %s to exclude %s (ignoring case) but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        expected = other.lower() if isinstance(other, str) else other
        actual = self._actual.lower() if isinstance(self._actual, str) else self._actual

        assert expected not in actual, msg

    def startswith(self, other):
        """Ensure that ``other`` starts the actual value."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = "Given text:\n\n%s\n\nExpected to start with %s but didn't" % (
                self._actual.strip(),
                repr(other),
            )
        else:
            msg = "Expected %s to start with %s but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert self._actual.startswith(other), msg

    def istartswith(self, other):
        """Same as ``startswith`` but ignoring case."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = (
                "Given text:\n\n%s\n\nExpected to start with %s (ignoring case) but didn't"
                % (self._actual.strip(), repr(other))
            )
        else:
            msg = "Expected %s to start with %s (ignoring case) but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert self._actual.lower().startswith(other.lower()), msg

    def endswith(self, other):
        """Ensure that ``other`` ends the actual value."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = "Given text:\n\n%s\n\nExpected to end with %s but didn't" % (
                self._actual.strip(),
                repr(other),
            )
        else:
            msg = "Expected %s to end with %s but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert self._actual.endswith(other), msg

    def iendswith(self, other):
        """Same as ``endswith`` but ignoring case."""
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable

        if isinstance(self._actual, str) and '\n' in self._actual:
            msg = (
                "Given text:\n\n%s\n\nExpected to end with %s (ignoring case) but didn't"
                % (self._actual.strip(), repr(other))
            )
        else:
            msg = "Expected %s to end with %s (ignoring case) but it didn't" % (
                repr(self._actual),
                repr(other),
            )

        assert self._actual.lower().endswith(other.lower()), msg

    @staticmethod
    def raises(expected_cls=Exception, message=None):
        """Ensure that an exception is raised.

        ::

            with expect.raises(MyCustomError):
                func_that_raises_error()

        is equivalent to:

        ::

            try:
                func_that_raises_error()
                raise AssertionError('Error not raised!')
            except MyCustomError:
                pass
        """
        return _RaisesExpectation(expected_cls, message)


class _RaisesExpectation:
    """
    Internal context decorator created when you do:
        with expect.raises(SomeError):
            something()
    """

    def __init__(self, exception_class, message):
        self._exception_class = exception_class
        self.message = message

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        success = not exc_type
        if success:
            raise AssertionError(
                'Expected an exception of type %s but got none'
                % self._exception_class.__name__
            )
        return self.validate_failure(exc_type, exc_value)

    def validate_failure(self, exc_type, exc_value):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        wrong_message_was_raised = self.message and self.message != str(exc_value)
        if wrong_message_was_raised:
            raise AssertionError(
                "Expected %s('%s') but got %s('%s')"
                % (
                    self._exception_class.__name__,
                    str(self.message),
                    exc_type.__name__,
                    str(exc_value),
                )
            )
        if issubclass(exc_type, self._exception_class):
            return True

        return None


class _CustomExpectation:
    """
    Internal class representing a single custom expectation. Don't create these
    directly; use `expecter.add_expectation` instead.
    """

    negative_verbs = {
        "can": "it can't",
        "is": "it isn't",
        "will": "it won't",
    }

    def __init__(self, predicate, actual):
        self._predicate = predicate
        self._actual = actual

    def __call__(self, *args, **kwargs):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        self.enforce(*args, **kwargs)

    def enforce(self, *args, **kwargs):
        __tracebackhide__ = _hidetraceback()  # pylint: disable=unused-variable
        if not self._predicate(self._actual, *args, **kwargs):
            predicate_name = self._predicate.__name__.replace('_', ' ')
            raise AssertionError(
                'Expected that %s %s, but %s'
                % (repr(self._actual), predicate_name, self._negative_verb())
            )

    def _negative_verb(self):
        # XXX: getting name in multiple places
        first_word_in_predicate = self._predicate.__name__.split('_')[0]
        try:
            return self.negative_verbs[first_word_in_predicate]
        except KeyError:
            return "got False"


_custom_expectations = {}


def add_expectation(predicate):
    """
    Add a custom expectation. After being added, custom expectations can be
    used as if they were built-in:

        >>> def is_long(x): return len(x) > 5
        >>> add_expectation(is_long)
        >>> expect('loooooong').is_long()
        >>> expect('short').is_long()
        Traceback (most recent call last):
        ...
        AssertionError: Expected that 'short' is_long, but it isn't

    The name of the expectation is taken from the name of the function (as
    shown above).
    """
    _custom_expectations[predicate.__name__] = predicate


def clear_expectations():
    """Remove all custom expectations"""
    _custom_expectations.clear()


def normalize(value):
    """Convert equivalent types for better diffs."""
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, OrderedDict) and sys.version_info >= (3, 6):
        return {k: normalize(v) for k, v in value.items()}
    return value


def normalized_diff(other, actual):
    diff = difflib.unified_diff(other.splitlines(), actual.splitlines(), lineterm='')
    diff = list(diff)  # type: ignore
    return '\n'.join(['\nDiff:'] + diff[2:])  # type: ignore


def _hidetraceback():
    return os.getenv('EXPECTER_HIDETRACEBACK')
