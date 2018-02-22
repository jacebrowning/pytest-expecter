You can use either import the function:

```python
from expecter import expect
```

Or use the fixture:

```python
def test_foobar(expect):
    expect("foo") != "bar"
```

