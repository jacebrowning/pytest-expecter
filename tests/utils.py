try:
    import builtins as __builtins__  # pylint: disable=redefined-builtin
except ImportError:
    import __builtin__ as __builtins__


str = getattr(__builtins__, 'unicode', str)  # pylint: disable=redefined-builtin


def fail_msg(callable_):
    try:
        callable_()
    except Exception as e:  # pylint: disable=broad-except
        return str(e)
    return None
