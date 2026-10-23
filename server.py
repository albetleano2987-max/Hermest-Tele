import os
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Jalankan gateway dan tangkap error-nya jika ada
def run_gateway():
    print("Starting Hermes Gateway thread...")
    try:
        process = subprocess.Popen(
            ["hermes", "gateway", "run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(f"[HERMES] {line}", end="", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to start gateway: {e}")

# 2. Jalankan di background thread
gateway_thread = threading.Thread(target=run_gateway, daemon=True)
gateway_thread.start()

# 3. Server HTTP mini untuk Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Agent is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"HTTP server listening on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
