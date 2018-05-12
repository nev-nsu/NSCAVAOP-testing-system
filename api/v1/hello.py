from api.handler import IHandler


class TApiCallHandler(IHandler):
    def handle(self, handler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text-html')
        handler.end_headers()
        handler.wfile.write(b"Hello world!")
        return
