from setuptools import setup

setup(
    name="pytest-expecter",
    version='0.2.2-1',
    description="A fork of 'expecter' with better support for pytest.",
    long_description=open("README.md").read(),
    author="Jace Browning",
    author_email="jacebrowning@gmail.com",
    py_modules=["expecter"],
    entry_points={
        "pytest11": [
            "pytest-expecter = expecter"
        ],
    },
    url="https://github.com/modustri/pytest-expecter",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
    ]
)
