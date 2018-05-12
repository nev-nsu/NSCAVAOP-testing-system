from multiprocessing.dummy import Pool
import metas
from config import SConfig


class SThreadPool(metaclass=metas.Singleton):
    def __init__(self):
        self.__thread_pool__ = Pool(SConfig().WORKERS)

    def add(self, task, args):
        self.__thread_pool__.apply_async(task, args)

    def terminate(self):
        self.__thread_pool__.terminate()
        self.__thread_pool__.join()
