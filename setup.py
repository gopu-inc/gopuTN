from setuptools import setup, find_packages

setup(
    name="gotn",
    version="0.2.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gotn=gotn.cli:main",
        ],
    },
)
