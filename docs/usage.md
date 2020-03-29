# Import

The `expect` utility can be imported from the package:

```python
from expecter import expect

def test_foobar():
    expect("foo") != "bar"
```

# Fixture

The utility is also available as `pytest` fixture

```python
def test_foobar(expect):
    expect("foo") != "bar"
```
