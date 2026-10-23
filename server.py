import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Jalankan Hermes Gateway di background
print("Starting Hermes Gateway...")
gateway_process = subprocess.Popen(["hermes", "gateway", "start"])

# 2. Server HTTP wajib untuk Render agar lolos deteksi port
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Agent is running!")

def run_server():
    # Render otomatis memberikan port lewat environment variable "PORT"
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"HTTP server listening on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
