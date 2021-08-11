"""
Initialize the logger for the custom resource
"""
import os
import sys
import logging

LOGGER = logging.getLogger('aws-auth0-cr')
LOGGER.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
HANDLER = logging.StreamHandler(sys.stdout)
FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
