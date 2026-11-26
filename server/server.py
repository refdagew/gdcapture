#!/usr/bin/env python3
"""Local GDCapture test server: browser WebSocket + Geode HTTP handshake."""
import asyncio
import json
import logging
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

HOST = "127.0.0.1"
WS_PORT = 8765
HTTP_PORT = 8766
MAX_MESSAGE_SIZE = 16 * 1024 * 1024

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class GeodeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/geode-loaded":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(min(length, 4096)).decode("utf-8", "replace")
        logging.info("GEODE MOD CONNECTED: %s", body)
        payload = json.dumps({"ok": True, "message": "GDCapture received Geometry Dash mod handshake"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        logging.info("HTTP " + fmt, *args)


async def handle_client(websocket):
    peer = websocket.remote_address
    logging.info("Browser connected: %s", peer)
    await websocket.send(json.dumps({
        "type": "server-ready",
        "message": "GDCapture local server is ready",
        "utc": datetime.now(timezone.utc).isoformat(),
    }))
    try:
        async for message in websocket:
            if isinstance(message, bytes):
                logging.info("Received binary payload: %d bytes", len(message))
                await websocket.send(message)
            else:
                logging.info("Received text: %s", message[:300])
                await websocket.send(json.dumps({"type": "echo", "message": message[:300]}))
    except ConnectionClosed:
        pass
    finally:
        logging.info("Browser disconnected: %s", peer)


async def main():
    http_server = ThreadingHTTPServer((HOST, HTTP_PORT), GeodeHandler)
    Thread(target=http_server.serve_forever, daemon=True).start()
    logging.info("Geode HTTP endpoint: http://%s:%d/geode-loaded", HOST, HTTP_PORT)
    logging.info("Browser WebSocket: ws://%s:%d", HOST, WS_PORT)
    try:
        async with serve(handle_client, HOST, WS_PORT, max_size=MAX_MESSAGE_SIZE,
                         ping_interval=20, ping_timeout=20):
            await asyncio.Future()
    finally:
        http_server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("GDCapture server stopped.")
