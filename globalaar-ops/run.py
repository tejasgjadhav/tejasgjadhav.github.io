"""Start GlobalAAR TPS Ops on the LAN and open a browser.

Usage:  python run.py [port]
Anyone on the factory network can then open  http://<this-pc-ip>:<port>
"""
import socket
import sys
import threading
import webbrowser

import uvicorn

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8035


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no traffic sent; just picks the LAN interface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    ip = lan_ip()
    print("=" * 56)
    print("  GlobalAAR TPS Ops")
    print(f"  This computer : http://localhost:{PORT}")
    print(f"  Factory LAN   : http://{ip}:{PORT}   <- share this URL")
    print("=" * 56)
    threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, log_level="warning")
