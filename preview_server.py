#!/usr/bin/env python3
"""
Simple preview server for EthernalLover
Serves static files and provides basic routing
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import urllib.parse

class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), 'public'), **kwargs)
    
    def do_GET(self):
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Route handling
        if path == '/' or path == '/index.html':
            self.path = '/index.html'
        elif path == '/characters' or path == '/characters.html':
            self.path = '/characters.html'
        elif path == '/character' or path == '/character.html':
            self.path = '/character.html'
        elif path.startswith('/style.css'):
            self.path = '/style.css'
        elif path.startswith('/auth.js'):
            self.path = '/auth.js'
        elif path.startswith('/app.js'):
            self.path = '/app.js'
        elif path.startswith('/chat.js'):
            self.path = '/chat.js'
        else:
            # Try to serve the file as-is
            pass
        
        return super().do_GET()
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PreviewHandler)
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         EthernalLover - Local Preview Server                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Server running at: http://localhost:{port}                  ║
║                                                              ║
║  Available pages:                                            ║
║  - Login:        http://localhost:{port}/                     ║
║  - Characters:   http://localhost:{port}/characters          ║
║  - Character:    http://localhost:{port}/character?id=1       ║
║                                                              ║
║  Note: API endpoints won't work without Vercel deployment   ║
║        This is a frontend preview only                      ║
║                                                              ║
║  Press Ctrl+C to stop the server                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.shutdown()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port)
