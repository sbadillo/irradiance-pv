from setuptools import setup

with open("irradiance_pv/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="irradiance_pv",
    version=1.2,
    description="Calculate in plane irradiance for a surface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["irradiance_pv"],
    author="Sergio Badillo",
    author_email="sbadilloworks@gmail.com",
    zip_safe=False,
)
