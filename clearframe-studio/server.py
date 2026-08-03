#!/usr/bin/env python3
"""ClearFrame Studio local server — static files + same-origin AI image proxy.

Pollinations.ai (free, keyless) rejects cross-origin browser requests (403)
but serves normal HTTP fine. Proxying through /img keeps every image
same-origin, so the canvas stays untainted and MediaRecorder can export
.webm files containing the real AI visuals.
"""
import http.server
import os
import urllib.parse
import urllib.request

PORT = 3462
POLLINATIONS = "https://image.pollinations.ai/prompt/"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/img?"):
            self.proxy_image()
            return
        super().do_GET()

    def proxy_image(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        prompt = qs.get("prompt", [""])[0]
        params = urllib.parse.urlencode(
            {k: qs[k][0] for k in ("width", "height", "seed", "nologo", "model", "enhance") if k in qs})
        url = POLLINATIONS + urllib.parse.quote(prompt) + "?" + params
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ClearFrameStudio/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            self.send_response(200)
            self.send_header("Content-Type", r.headers.get("Content-Type", "image/jpeg"))
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(502, f"image proxy failed: {e}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print(f"ClearFrame Studio serving on http://localhost:{PORT}")
    server.serve_forever()
