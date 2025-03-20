from setuptools import setup, find_packages

with open("requirements.txt") as requirement_file:
    requirements = requirement_file.read().split()

setup(
    name="model_creator",
    description="A package to create a model from a dataset.",
    version="1.0.0",
    author="Mohamed Ghallab",
    author_email="ghallab98@gmail.com",
    install_requires=requirements,
    packages=find_packages(),
)