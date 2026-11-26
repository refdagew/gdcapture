#!/usr/bin/env python3
"""Local GDCapture WebSocket test server.

Listens on loopback only. Text messages are echoed; binary messages are
echoed unchanged so the browser/mod can test the transport without encoding.
"""
import asyncio
import json
import logging
from datetime import datetime, timezone

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

HOST = "127.0.0.1"
PORT = 8765
MAX_MESSAGE_SIZE = 16 * 1024 * 1024

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


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
                await websocket.send(json.dumps({
                    "type": "echo",
                    "message": message[:300],
                }))
    except ConnectionClosed:
        pass
    finally:
        logging.info("Browser disconnected: %s", peer)


async def main():
    logging.info("Starting GDCapture server on ws://%s:%d", HOST, PORT)
    async with serve(
        handle_client,
        HOST,
        PORT,
        max_size=MAX_MESSAGE_SIZE,
        ping_interval=20,
        ping_timeout=20,
    ):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped.")
