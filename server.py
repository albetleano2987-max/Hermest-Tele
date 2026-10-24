import os
import json
from http.server import BaseHTTPRequestHandler

# Impor modul dari Hermes Agent Anda jika ingin dihubungkan langsung
# Contoh: from hermes_core import process_telegram_update

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Baca ukuran data yang masuk dari Telegram
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 2. Ubah data mentah menjadi format JSON (Dictionary Python)
            update = json.loads(post_data.decode('utf-8'))

            # (Opsional) Debugging data masuk ke log Vercel
            print("Incoming Telegram Update:", json.dumps(update))

            # 3. Panggil fungsi utama Hermes Agent Anda di sini
            # process_telegram_update(update)

            # 4. Kirim respons sukses 200 OK kembali ke server Telegram
            # Ini wajib agar Telegram tahu pesannya sudah diterima dengan baik
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

        except Exception as e:
            # Jika terjadi error, kirim respons 500 dan cetak error-nya di log Vercel
            print(f"Error processing webhook: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_GET(self):
        # Endpoint GET untuk memastikan bahwa URL Vercel aktif saat dikunjungi via browser
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Agent Webhook is active and running on Vercel!")
