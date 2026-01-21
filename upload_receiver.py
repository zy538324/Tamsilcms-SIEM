# upload_receiver.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import os, time

class Receiver(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        now = int(time.time())
        outdir = os.path.join('received_uploads')
        os.makedirs(outdir, exist_ok=True)
        fname = os.path.join(outdir, f'upload_{now}.bin')
        with open(fname, 'wb') as f:
            f.write(body)
        print(f"Saved {fname} ({len(body)} bytes) Headers: {self.headers}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

if __name__ == '__main__':
    print('Listening on http://0.0.0.0:8000/upload')
    HTTPServer(('0.0.0.0', 8000), Receiver).serve_forever()