import json
import importlib
from http.server import BaseHTTPRequestHandler, HTTPServer

class HttpHandler(BaseHTTPRequestHandler):

    def _response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        """Handle GET requests"""
        self._handle_request("GET")

    def do_POST(self):
        """Handle POST requests"""
        self._handle_request("POST")

    def do_PUT(self):
        """Handle PUT requests"""
        self._handle_request("PUT")

    def do_DELETE(self):
        """Handle DELETE requests"""
        self._handle_request("DELETE")

    def _handle_request(self, method):
        """Dynamically route requests to the correct controller and method"""
        # z.B: /user/get
        path_parts = self.path.strip('/').split('/')  
        #[user,get]
        if len(path_parts) < 2:
            self._response(400, {"error": "Invalid request. Use /Controller/Method"})
            return

        controller_name, method_name = path_parts[:2]  

        try:
            controller_name = controller_name.capitalize() # user => User
            controller_name = controller_name+"Controller" #=> User => UserController
            module = importlib.import_module(f'controller.{controller_name}')  # Import UserController
            controller_class = getattr(module, controller_name)  # Get class
            controller_instance = controller_class()  # Instantiate controller = UserController() 

            if not hasattr(controller_instance, method_name):
                self._response(404, {"error": f"Method '{method_name}' not found in {controller_name}"})
                return

            method_to_call = getattr(controller_instance, method_name)  # z.B Get method get

            data = None
            if method in ["POST", "PUT"]:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                try:
                    data = json.loads(post_data)
                except json.JSONDecodeError:
                    self._response(400, {"error": "Invalid JSON format"})
                    return

            result = method_to_call(data) if method in ["POST", "PUT"] else method_to_call()
            self._response(200, {"success": True, "data": result})

        except ModuleNotFoundError:
            self._response(404, {"error": f"Controller '{controller_name}' not found"})
        except Exception as e:
            self._response(500, {"error": str(e)})

def run(server_class=HTTPServer, handler_class=HttpHandler, port=8001):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

