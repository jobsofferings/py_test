from http.server import BaseHTTPRequestHandler
from app import start_web

class handler(BaseHTTPRequestHandler):

    result = start_web()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('AI deploy test 200'.encode('utf-8'))
        return