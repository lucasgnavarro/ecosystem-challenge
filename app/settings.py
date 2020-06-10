from os import pardir
from os.path import dirname, join, realpath

PROJECT_ROOT = join(dirname(realpath(__file__)), pardir)

# Temporary folder
TEMP_FOLDER = join(PROJECT_ROOT, 'tmp')
