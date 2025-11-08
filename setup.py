from setuptools import setup, find_packages

setup(
    name="gotn",
    version="0.1.0",
    description="CLI pour gopuTN, un langage simplifié inspiré de Docker",
    author="Ceose",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gotn=gotn.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

