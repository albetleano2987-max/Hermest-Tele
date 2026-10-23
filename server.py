import os
import threading
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Fungsi untuk menjalankan Hermes Gateway di background thread dengan unbuffered output
def run_gateway():
    print("Starting Hermes Gateway thread...")
    process = subprocess.Popen(
        ["hermes", "gateway", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    # Teruskan log gateway langsung ke terminal Render secara real-time
    for line in process.stdout:
        print(line, end="", flush=True)

# 2. Jalankan gateway di thread terpisah agar tidak memblokir server HTTP
gateway_thread = threading.Thread(target=run_gateway, daemon=True)
gateway_thread.start()

# 3. Server HTTP mini untuk memenuhi aturan port Render
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
