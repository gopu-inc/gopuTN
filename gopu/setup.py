from setuptools import setup, find_packages

setup(
    name="gopu",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gotn = gopu.cli:main",
        ],
    },
    install_requires=["requests"],  # ajoute tes dépendances
)
