"""Uçtan uca testler için gerçek sunucu: uvicorn boş bir portta, ayrı bir thread'de çalışır."""
import socket
import threading
import time

import pytest
import uvicorn

from api import app


def _bos_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def canli_sunucu():
    port = _bos_port()
    sunucu = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=sunucu.run, daemon=True)
    thread.start()
    while not sunucu.started:
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    sunucu.should_exit = True
    thread.join(timeout=5)
