import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class HttpHandler(BaseHTTPRequestHandler):

    def _response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        response = {"message": "GET request received hiiii"}
        self._response(200, response)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            response = {"message": "POST received successfully", "data": data}
            self._response(201, response)
        except json.JSONDecodeError:
            self._response(400, {"error": "data is not in valid JSON format"}) 

def run(port=8001):
        server_class = HTTPServer
        handler_class = HttpHandler
        server_address = ('', port)  # Listen on all interfaces
        httpd = server_class(server_address, handler_class)
        print(f"Server running on port {port}...")
        httpd.serve_forever()