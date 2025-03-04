# Constants

## Anything

The `expect.anything` constant can be used ignore elements of a nested structure in equality comparisons:

```python
response = request.get('http://example.com/api')
expect(response.json()) == {
    'id': expect.anything,
    'name': 'Jane Doe',
}
```
