import metas
from config import SConfig
from multiprocessing.dummy import Pool

class SThreadPool(metaclass=metas.Singleton):
    def __init__(self):
        self.__threadPool__ = Pool(SConfig().WORKERS)
    
    def addTask(self, task, args):
        self.__threadPool__.apply_async(task, args)
    
    def terminate(self):
        self.__threadPool__.terminate()
        self.__threadPool__.join()

