#!/usr/bin/env python3
import asyncio
from hypercorn import Config
from hypercorn.asyncio import serve
from pycrdt.websocket import ASGIServer, WebsocketServer
from speasy_proxy.config import collab_endpoint
import os


async def main():
    websocket_server = WebsocketServer()
    app = ASGIServer(websocket_server)
    config = Config()
    config.bind = [f"localhost:{collab_endpoint.port()}"]
    async with websocket_server:
        await serve(app, config, mode="asgi")

asyncio.run(main())