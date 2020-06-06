# Equality

```python
expect(42) == 42
expect(42) != 0
```

# Comparison

```python
expect(42) > 0
expect(1.2) <= 1.23
```

# Contents

```python
expect("Hello, world!").contains("world")  # or 'includes'
expect("Hello, world!").excludes("foobar")  # or 'does_not_contain'
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

# Identity

```python
expect(value).is_(True)
expect(value).is_(False)
expect(value).is_(None)
expect(value).is_not(True)
expect(value).is_not(False)
expect(value).is_not(None)
```

# Exceptions

```python
with expect.raises(ValueError):
    int("abc")

with expect.raises(RuntimeError, "'dog' cannot 'quack'"):
    animal = 'dog'
    verb = 'quack'
    raise RuntimeError("{!r} cannot {!r}".format(animal, verb))
```
