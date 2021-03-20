from setuptools import setup
from os import path

# read the contents of your README file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="irradiance_pv",
    version=1.24,
    description="Calculate in plane irradiance for a surface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["irradiance_pv"],
    author="Sergio Badillo",
    author_email="sbadilloworks@gmail.com",
    zip_safe=False,
)
