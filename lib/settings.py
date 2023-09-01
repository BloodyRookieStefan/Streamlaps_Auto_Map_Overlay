############################################################################
# Parsing user settings
# Date: 01.09.2023
############################################################################

import os, configparser

# Define settings
Settings = configparser.ConfigParser()
# Build ini path
f = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..' , 'autooverlay.ini')
# Check if file exists
if not os.path.isfile(f):
    raise FileNotFoundError(f'Missing file {f}')
# Read settings
Settings.read(f)