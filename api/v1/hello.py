from api import api

class TApiCallHandler(api.IHandler):
    def handle(self, TRequestHandler):
        TRequestHandler.send_response(200)
        TRequestHandler.send_header('Content-type','text-html')
        TRequestHandler.end_headers()
        TRequestHandler.wfile.write(b"Hello world!")
        return
