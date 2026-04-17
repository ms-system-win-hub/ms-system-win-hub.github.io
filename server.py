#!/usr/bin/env python3
"""带 COOP/COEP 头的 HTTP 服务器，用于 ffmpeg.wasm"""

import http.server
import socketserver

class COOPHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # ffmpeg.wasm 需要这两个头才能使用 SharedArrayBuffer
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        # 允许 eval 和 wasm 编译
        self.send_header('Content-Security-Policy', 
            "default-src 'self'; "
            "script-src 'self' 'unsafe-eval' 'wasm-unsafe-eval' blob:; "
            "worker-src 'self' blob:; "
            "connect-src 'self' blob: data:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: blob:"
        )
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {args[0]}")

if __name__ == '__main__':
    PORT = 8888
    with socketserver.TCPServer(("", PORT), COOPHandler) as httpd:
        print(f"🎵 WAVFORM 服务器运行在 http://localhost:{PORT}/")
        print("   已启用 COOP/COEP 头，支持 ffmpeg.wasm")
        print("   按 Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
