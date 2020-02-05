def fail_msg(callable_):
    try:
        callable_()
    except Exception as e:  # pylint: disable=broad-except
        return str(e)
    return None
