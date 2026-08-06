#!/usr/bin/env python3
"""Launch a lightweight local server for the V5.0 Beta dashboard."""

from __future__ import annotations

import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "results" / "v5" / "v5.0_baseline"


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler)
    print(f"V5.0 Beta dashboard ready at http://127.0.0.1:{port}/dashboard/index.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard server stopped.")


if __name__ == "__main__":
    main()
