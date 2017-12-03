```python
from expecter import expect
```

# Equality

```python
expect(42) == 42
expect(42) != 0
```

# Comparison

```python
expect(42) > 0
```

# Contents

```python
expect("Hello, world!").contains("world")
expect("Hello, world!").excludes("foobar")  # or does_not_contain
```

# Types

```python
expect(4.2).isinstance(float)
```

# Exceptions

```python
with expect.raises(ValueError):
    int("abc")
```

