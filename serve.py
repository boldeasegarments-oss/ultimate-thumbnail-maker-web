import http.server
import socketserver
import os
import urllib.parse
import sys

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class RobustNoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def translate_path(self, path):
        # 1. Normalize path: strip scheme and host if present
        if path.startswith('http://') or path.startswith('https://'):
            parsed = urllib.parse.urlparse(path)
            path = parsed.path or '/'

        # 2. Strip leading /Videos/ASASO or /ASASO if requested through proxy or nested path
        if path.startswith('/Videos/ASASO/'):
            path = path[len('/Videos/ASASO'):]
        elif path.startswith('/ASASO/'):
            path = path[len('/ASASO'):]

        # 3. Clean up query strings and fragments
        path = path.split('?')[0].split('#')[0]

        # 4. Use standard translate_path
        translated = super().translate_path(path)

        # 5. If directory requested and index.html exists, serve it
        if os.path.isdir(translated):
            index_path = os.path.join(translated, 'index.html')
            if os.path.exists(index_path):
                return index_path

        return translated

    def translate_path(self, path):
        if path.startswith('http://') or path.startswith('https://'):
            from urllib.parse import urlparse
            path = urlparse(path).path
        return super().translate_path(path)

    def end_headers(self):
        # Prevent any caching on localhost
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Flush stdout immediately so logs appear in real-time
        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))
        sys.stdout.flush()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    print(f"Starting robust web server from: {BASE_DIR}")
    with socketserver.TCPServer(("", PORT), RobustNoCacheHTTPRequestHandler) as httpd:
        print(f"Serving HTTP on port {PORT} (no-cache, robust path translation enabled)")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
