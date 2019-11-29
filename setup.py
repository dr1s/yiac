from setuptools import setup

setup(
    name="yiac",
    version="0.1.dev0",
    url="https://github.com/dr1s/yiac",
    author="Daniel Schmitz",
    license="MIT",
    description="Xiaomi Yi Python API",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["yiac=yiac.cli:main"]},
)
