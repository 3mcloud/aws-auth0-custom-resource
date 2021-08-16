# setup.py
"""
Setup tools
"""
from setuptools import setup, find_packages

NAME = 'aws_auth0_custom_resource'
VERSION = '0.1'
AUTHOR = 'Eric Walker'
AUTHOR_EMAIL = 'erictwalker18@gmail.com'
DESCRIPTION = 'AWS Custom Resource for Auth0 Resources'
URL = 'https://github.com/3mcloud/aws-auth0-custom-resource'
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
    'boto3',  # boto3 is included in lambda runtime
]

LONG_DESCRIPTION = 'Auth0 resources custom resource'

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
        'dev': REQUIRES_TEST
    },
    include_package_data=True
)
