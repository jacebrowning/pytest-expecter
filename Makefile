.phony: upload
upload:
	pandoc -f markdown_github -t rst -o README.rst README.md
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel
	pipenv run twine upload dist/*.*
