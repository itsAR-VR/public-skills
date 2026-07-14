"""Standalone HTTP file server for DLNA media streaming."""

import socket
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Quiet HTTP request handler that doesn't log requests."""

    def __init__(self, *args, directory=None, **kwargs):
        self.directory = directory
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        pass


class MediaServer:
    """HTTP server for serving media files to DLNA devices."""

    def __init__(self, directory: Path, port: int = 0):
        self.directory = directory
        self.port = port
        self._server: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._actual_port: int = 0

    def start(self) -> int:
        """Start the HTTP server. Returns the actual port."""
        handler = lambda *args, **kwargs: QuietHTTPRequestHandler(
            *args, directory=str(self.directory), **kwargs
        )
        self._server = HTTPServer(("0.0.0.0", self.port), handler)
        self._actual_port = self._server.server_address[1]

        def serve():
            self._server.serve_forever()

        self._thread = threading.Thread(target=serve, daemon=True)
        self._thread.start()
        return self._actual_port

    def stop(self):
        """Stop the HTTP server."""
        if self._server:
            self._server.shutdown()
            self._server = None

    @property
    def url(self) -> str:
        """Get the base URL for the server."""
        local_ip = _get_local_ip()
        return f"http://{local_ip}:{self._actual_port}"


def _get_local_ip() -> str:
    """Get local IP address suitable for LAN access."""
    # Method 1: UDP socket to external host (works when internet is available)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith("127."):
            return ip
    except Exception:
        pass

    # Method 2: hostname resolution (works on many LAN setups)
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if not ip.startswith("127."):
            return ip
    except Exception:
        pass

    # Method 3: broadcast address scan (isolated LAN without internet)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith("127."):
            return ip
    except Exception:
        pass

    # Method 4: enumerate all addresses via hostname; pick first non-loopback
    try:
        _, _, addresses = socket.gethostbyname_ex(socket.gethostname())
        for ip in addresses:
            if not ip.startswith("127."):
                return ip
    except Exception:
        pass

    print(
        "warning: could not determine non-loopback IP; DLNA renderers "
        "will not be able to reach 127.0.0.1",
        file=sys.stderr,
    )
    return "127.0.0.1"
