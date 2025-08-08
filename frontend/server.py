#!/usr/bin/env python3
"""
Simple web server for the Movember Impact Dashboard
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_server(port=3000):
    """Run the web server."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)

    print(f"🌐 Movember Impact Dashboard")
    print(f"📊 Server running at: http://localhost:{port}")
    print(f"🔗 API endpoint: http://localhost: 8000")
    print(f"📱 Open your browser and navigate to: http://localhost:{port}")
    print(f"⏹️  Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        httpd.server_close()

if __name__ == "__main__":
    port = 3000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 3000.")

    run_server(port)
