import os
import json
from http.server import BaseHTTPRequestHandler
import redis

# 1. Ambil kredensial Upstash Redis dari Environment Variables Vercel
UPSTASH_REDIS_REST_URL = os.environ.get("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN")

# Inisialisasi koneksi Redis untuk memori jangka panjang
r = None
if UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN:
    r = redis.Redis(
        host=UPSTASH_REDIS_REST_URL.replace("https://", "").replace("http://", ""),
        port=6379,
        ssl=True,
        password=UPSTASH_REDIS_REST_TOKEN
    )

def get_chat_history(chat_id):
    """Mengambil riwayat memori chat dari Upstash Redis"""
    if r:
        stored = r.get(f"chat_history:{chat_id}")
        if stored:
            return json.loads(stored.decode('utf-8'))
    return []

def save_chat_history(chat_id, history):
    """Menyimpan riwayat memori chat terbaru ke Upstash Redis (maksimal 12 pesan terakhir)"""
    if r:
        r.set(f"chat_history:{chat_id}", json.dumps(history[-12:]))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 2. Baca data pesan masuk (payload) dari Telegram
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data.decode('utf-8'))

            if "message" in update:
                chat_id = str(update["message"]["chat"]["id"])
                text = update["message"].get("text", "")

                # 3. Tarik memori lama berdasarkan chat_id agar bot tidak lupa ingatan
                history = get_chat_history(chat_id)

                # --- 4. Masukkan fungsi / logika utama Hermes Agent Anda di sini ---
                # Contoh:
                # response_text = hermes_process(text, history)
                response_text = f"Pesan diterima dengan memori aktif! Anda berkata: {text}"
                # ------------------------------------------------------------------

                # 5. Masukkan interaksi terbaru ke dalam riwayat memori
                history.append({"role": "user", "content": text})
                history.append({"role": "assistant", "content": response_text})

                # 6. Simpan kembali memori yang telah diperbarui ke Upstash Redis
                save_chat_history(chat_id, history)

            # 7. Kirim respons sukses 200 OK ke Telegram
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Agent Webhook with Redis Memory is active!")
