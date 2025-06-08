from speasy_proxy.config import collab_endpoint
import logging

log = logging.getLogger(__name__)

if collab_endpoint.enable():
    from asyncio import create_task
    from anyio import get_cancelled_exc_class, Lock
    from contextlib import asynccontextmanager
    from fastapi import WebSocket
    from httpx_ws import aconnect_ws
    from pycrdt import Array, Doc, Provider
    from pycrdt.websocket import WebsocketServer
    from pycrdt.websocket.websocket import HttpxWebsocket
    from .routes import router


    class Websocket:
        def __init__(self, websocket, path: str):
            self._websocket = websocket
            self._path = path
            self._send_lock = Lock()

        @property
        def path(self) -> str:
            return self._path

        def __aiter__(self):
            return self

        async def __anext__(self) -> bytes:
            try:
                message = await self.recv()
            except Exception:
                raise StopAsyncIteration()
            return message

        async def send(self, message: bytes):
            async with self._send_lock:
                await self._websocket.send_bytes(message)

        async def recv(self) -> bytes:
            b = await self._websocket.receive_bytes()
            return bytes(b)


    @asynccontextmanager
    async def aprovider_factory(port, room_name, ydoc=None, log=None):
        ydoc = Doc() if ydoc is None else ydoc
        server_websocket = None
        connect = aconnect_ws(f"http://localhost:{port}/{room_name}")
        try:
            async with connect as websocket:
                websocket_provider = Provider(ydoc, Websocket(websocket, room_name), log)
                async with websocket_provider as websocket_provider:
                    yield ydoc, server_websocket
        except get_cancelled_exc_class():
            pass


    def provider_factory(path, doc, log):
        return aprovider_factory(collab_endpoint.port(), path, ydoc=doc, log=log)


    @router.websocket("/collaboration/{path:path}")
    async def websocket_endpoint(path: str, websocket: WebSocket):
        await websocket.accept()
        websocket_server = await get_websocket_server()
        await websocket_server.serve(HttpxWebsocket(websocket, path))


    async def get_websocket_server():
        global WEBSOCKET_SERVER
        if WEBSOCKET_SERVER is None:
            WEBSOCKET_SERVER = WebsocketServer(provider_factory=provider_factory)
            create_task(WEBSOCKET_SERVER.start())
            await WEBSOCKET_SERVER.started.wait()
        return WEBSOCKET_SERVER


    WEBSOCKET_SERVER = None

else:
    log.info(f'Collaboration endpoint is disabled, set {collab_endpoint.enable.env_var_name} to True to enable it')
