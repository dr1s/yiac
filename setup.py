import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="yiac",
    version="0.1.dev1",
    url="https://github.com/dr1s/yiac",
    author="Daniel Schmitz",
    license="MIT",
    description="Xiaomi Yi Python API",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["yiac=yiac.cli:main"]},
    packages=find_packages(),
)
