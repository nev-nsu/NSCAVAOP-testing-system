from .. import api

class TApiCallHandler(api.IHandler):
    def handle(self, TRequestHandler):
        TRequestHandler.send_response(200)
        TRequestHandler.wfile.write(b"Hello world!")
        return
