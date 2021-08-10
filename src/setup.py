# setup.py
'''
Setup tools
'''
import re
import subprocess
from shutil import which
from setuptools import setup, find_packages

NAME = 'aws_cr_authn'
VERSION = '0.1'
AUTHOR = 'Eric Walker'
AUTHOR_EMAIL = 'ewalker3@mmm.com'
DESCRIPTION = 'AWS Custom Resource for authentication resouruces'
URL = 'https://github.mmm.com/MMM/aws-cr-authn'
REQUIRES = [
    'auth0-python',
    'stringcase',
    'cerberus',
    'crhelper'
]
REQUIRES_TEST = [
    'PyYAML>=5.3.1',
    'pylint>=2.5.0',
    'pytest>=5.4.1',
    'pytest-cov>=2.8.1',
    'bandit>=1.6.2',
    'safety>=1.8.7',
    'paste',
    'ptvsd',
    'boto3',
]

REQUIRES_DOCS = [

]
LONG_DESCRIPTION = 'Auuthentication resources custom resource'

# Probably don't need to edit below this line

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=REQUIRES,
    extras_require={
        'dev': REQUIRES_TEST,
        'docs': REQUIRES_DOCS,
    },
    include_package_data=True
)
