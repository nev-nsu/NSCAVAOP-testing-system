import os
import metas


class SConfig(metaclass=metas.Singleton):
    def __init__(self):
        self.DEFAULT_PORT = 8080
        self.DEFAULT_PAGE = 'projects.html'
        self.WORKERS = 2
        self.STATIC_PATH = os.path.abspath(
            os.path.dirname(__file__)) + '/static'
        self.TEMP_DIR = os.path.abspath(os.path.dirname(__file__)) + '/tmp'
        self.SANDBOX_PROFILE = os.path.abspath(
            os.path.dirname(__file__)) + '/kernel/default.profile'
        self.DATABASE='pq://nev:123@localhost:5432/nscvaop'

