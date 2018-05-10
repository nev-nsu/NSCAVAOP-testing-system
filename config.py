import os

DEFAULT_PORT = 8080
DEFAULT_PAGE = 'index.html'
WORKERS = 2

STATIC_PATH = os.path.abspath(os.path.dirname(__file__)) + '/static'
TEMP_DIR = os.path.abspath(os.path.dirname(__file__)) + '/tmp'
SANDBOX_PROFILE = os.path.abspath(os.path.dirname(__file__)) + '/kernel/default.profile'
