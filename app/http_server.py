import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'
HTTP_PORT = 3000

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = f'/{TEMPLATES_DIR}/index.html'
        elif self.path == '/message':
            self.path = f'/{TEMPLATES_DIR}/message.html'
        elif self.path.startswith('/static/'):
            self.path = self.path.lstrip('/')
        else:
            self.path = f'/{TEMPLATES_DIR}/error.html'
            self.send_response(404)

        return super().do_GET()



def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, Handler)
    print(f"HTTP сервер запущений на порту {server_address[1]}")
    httpd.serve_forever()


if __name__ == '__main__':
    run_http_server()
