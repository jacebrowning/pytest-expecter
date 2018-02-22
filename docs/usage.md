# Import

The `expect` utility can be imported as normal:

```python
from expecter import expect
```

# Fixture

A `pytest` fixture is also available:

```python
def test_foobar(expect):
    expect("foo") != "bar"
```

