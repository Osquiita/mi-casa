# -*- coding: utf-8 -*-
"""Cliente TCP para la extension sketchup-mcp2 (puerto 9876).

Mismo patron que blender_client.py: no depende del reinicio de opencode.
Protocolo: JSON-RPC 2.0, prefijo de longitud de 4 bytes big-endian,
handshake 'hello' con client_version 0.3.0 (exact-match con el .rbz).
"""
import socket
import struct
import json
import sys

HOST = "127.0.0.1"
PORT = 9876
CLIENT_VERSION = "0.3.0"


def _send_frame(sock, obj):
    body = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack(">I", len(body)) + body)


def _recv_frame(sock):
    header = _recv_exact(sock, 4)
    (length,) = struct.unpack(">I", header)
    if length == 0:
        raise RuntimeError("frame de longitud cero")
    return json.loads(_recv_exact(sock, length))


def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise EOFError("conexion cerrada")
        buf += chunk
    return buf


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None
        self.next_id = 0

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=10)
        self.sock.settimeout(300)
        _send_frame(self.sock, {
            "jsonrpc": "2.0",
            "method": "hello",
            "params": {"client_version": CLIENT_VERSION},
            "id": 0,
        })
        resp = _recv_frame(self.sock)
        if "error" in resp:
            raise RuntimeError(f"handshake: {resp['error']}")
        return resp.get("result", {})

    def send(self, name, args=None):
        self.next_id += 1
        rid = self.next_id
        _send_frame(self.sock, {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": name, "arguments": args or {}},
            "id": rid,
        })
        resp = _recv_frame(self.sock)
        if resp.get("id") != rid:
            raise RuntimeError(f"id mismatch: {resp}")
        if "error" in resp:
            err = resp["error"]
            raise RuntimeError(f"{name}: code={err.get('code')} msg={err.get('message')}")
        result = resp.get("result", {})
        if isinstance(result, dict) and "content" in result:
            texts = []
            for item in result["content"]:
                if isinstance(item, dict) and "text" in item:
                    texts.append(item["text"])
            return "\n".join(texts)
        return result

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None


if __name__ == "__main__":
    verb = sys.argv[1] if len(sys.argv) > 1 else "get_version"
    args_raw = sys.argv[2] if len(sys.argv) > 2 else None
    args = json.loads(args_raw) if args_raw else {}
    c = Client()
    try:
        c.connect()
        print(json.dumps(c.send(verb, args), ensure_ascii=False))
    finally:
        c.close()