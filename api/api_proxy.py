from os import sep, path, listdir
import glob
import sys
import metas


class SApiProxy(metaclass=metas.Singleton):
    def __init__(self):
        self.handlers = {}
        dir = path.dirname(__file__)
        for file in listdir(dir):
            full_path = path.join(dir, file)
            if path.isdir(full_path):
                modules = glob.glob(full_path + sep + "*.py")
                modules = [f for f in modules if path.isfile(
                    f) and not path.basename(f).startswith('_')]
                modules = [
                    'api.' +
                    file +
                    '.' +
                    path.basename(f)[
                        :-
                        3] for f in modules]
                for module_name in modules:
                    __import__(module_name)
                    self.handlers[module_name] = sys.modules[module_name].TApiCallHandler(
                    )

    def handle(self, api_path, handler):
        api_path = api_path.replace('/', '.').strip('.')
        if api_path not in self.handlers:
            handler.send_error(404, 'Api Not Found')
            return
        try:
            self.handlers[api_path].handle(handler)
        except Exception as e:
            handler.send_error(500, 'Internal Server Error')
            print(str(e))
