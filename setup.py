# Import modules
from setuptools import setup, find_packages

# Configure the setup for the package
setup(
    name="interview-question-creator",
    version="0.0.0",
    author="Saurav Sabu",
    author_email="saurav.sabu9@gmail.com",
    description="A tool to create interview questions",
    packages=find_packages(), # Automatically find and include all packages in the project
    install_requires=[] # List of dependencies required by the package
)