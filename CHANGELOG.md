# Release Notes

## 3.0 (2025-03-04)

- Dropped support for Python 3.6 and 3.7.

## 2.3 (2022-01-20)

- Updated the representation of `expect.anything` to simplify diffs.

## 2.2 (2020-07-08)

- Added support for matching non-identity via `expect(actual).is_not(expected)`.
- Added `expect.anything` constant to ignore parts of a nested structure.

## 2.1 (2020-03-29)

- Added support for matching identity via `expect(actual).is_(expected)`.
- Added `includes` helper as an alias of `contains`.

## 2.0 (2020-02-06)

- Dropped Python 2 support.
- Added support for Python 3.8.

## 1.3 (2018-08-10)

- Added `startswith`, `endswith`, `istartswith`, and `iendswith` helpers.
- Added support for Python 3.7.

## 1.2 (2018-03-17)

- Added `icontains` method to check for containment ignoring case.
- Added `iexcludes` method to check for exclusion ignoring case.

## 1.1 (2018-02-21)

- Added `expect` fixture to use directly in tests.

## 1.0 (2017-12-03)

- Initial stable release.

## 0.2.2.post7 (2017-12-02)

- Added automatic conversion from `OrderedDict` to `dict` on Python 3.6 to create readable diffs.
