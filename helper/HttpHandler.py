import json
import importlib
from http.server import HTTPServer, BaseHTTPRequestHandler
"""
Note: This class is not suitable for production.

It is designed solely for educational purposes to demonstrate how HTTP requests work. There are several areas that could be cleaner, more optimized, and more secure for a production-level application.

This class is intended for beginners to understand the HTTP request lifecycle and gain insights into how robust frameworks like Flask and Django handle requests efficiently.

"""
class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._handle_request("GET")

    def do_POST(self):
        self._handle_request("POST")

    def do_PUT(self):
        self._handle_request("PUT")

    def do_DELETE(self):
        self._handle_request("DELETE")

    def _handle_request(self, method_HTTP):
        controller_name, method_name = self._validateRequestParts()
        if isinstance(controller_name, dict):  # Error case from `_validateRequestParts`
            return self._send_response(400, controller_name)

        try:
            controller_instance = self._createInstance(controller_name)
            if not controller_instance:
                return self._send_response(404, {"error": f"Controller '{controller_name}' not found."})

            method_to_call = self._createMethod(controller_instance, method_name)
            if not method_to_call:
                return self._send_response(404, {"error": f"Method '{method_name}' not found in '{controller_name}'."})

            data = self._load_data(method_HTTP)
            response_data = method_to_call(data) if method_HTTP in ["POST", "PUT"] else method_to_call()
            status_code = response_data.get("status_code", 200)
            return self._send_response(status_code, response_data)
        except Exception as e:
            return self._send_response(500, {"error": str(e)})

    def _validateRequestParts(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) < 2:
            return {"error": "Invalid request. Use /Controller/Method"}

        controller_name, method_name = path_parts[:2]
        controller_name = controller_name.capitalize() + "Controller"
        return controller_name, method_name

    def _createInstance(self, controller_name):
        try:
            module = importlib.import_module(f'controller.{controller_name}')
            controller_class = getattr(module, controller_name, None)
            if controller_class is None:
                return None
            return controller_class()
        except ImportError:
            return None

    def _createMethod(self, controller_instance, method_name):
        return getattr(controller_instance, method_name, None)

    def _load_data(self, HTTP_method):
        if HTTP_method in ["POST", "PUT"]:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                return json.loads(post_data)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON format"}
        return None

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

def run(port=8001):
    server_class = HTTPServer
    handler_class = HttpHandler
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()
