import os
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Fungsi untuk menjalankan Hermes Gateway di thread latar belakang
def run_gateway():
    print("Starting Hermes Gateway...")
    subprocess.run(["hermes", "gateway", "run"])

# 2. Jalankan gateway menggunakan thread terpisah agar tidak memblokir server HTTP
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
