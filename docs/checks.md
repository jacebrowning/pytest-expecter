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
expect("Hello, world!").icontains("hello")
expect("Hello, world!").iexcludes("FOOBAR")
```

# Strings

```python
expect("Hello, world!").startswith("Hello")
expect("Hello, world!").endswith("world!")
expect("Hello, world!").istartswith("hello")
expect("Hello, world!").iendswith("WORLD!")
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

