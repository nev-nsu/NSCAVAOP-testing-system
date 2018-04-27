import os

DEFAULT_PORT = 8080
STATIC_PATH = os.path.abspath(os.path.dirname(__file__)) + '/static'
DEFAULT_PAGE = 'index.html'
TEMP_DIR = os.path.abspath(os.path.dirname(__file__)) + '/tmp'
SANDBOX_PROFILE = os.path.abspath(os.path.dirname(__file__)) + '/sandbox/default.profile'
