.phony: upload
upload:
	pandoc -f markdown_github -t rst -o README.rst README.md
	python setup.py register --strict
	python setup.py sdist upload
	python setup.py bdist_wheel upload
