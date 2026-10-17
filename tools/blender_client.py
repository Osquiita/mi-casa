# -*- coding: utf-8 -*-
"""Cliente para enviar comandos al addon BlenderMCP (puerto 9876)."""
import socket
import json
import sys


def send(payload, timeout=180):
    data = json.dumps(payload) + "\n"
    s = socket.create_connection(("localhost", 9876), timeout=10)
    s.sendall(data.encode())
    chunks = []
    s.settimeout(timeout)
    try:
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
            buf = b"".join(chunks)
            try:
                json.loads(buf.decode(errors="replace"))
                break
            except Exception:
                continue
    except socket.timeout:
        pass
    s.close()
    raw = b"".join(chunks).decode(errors="replace")
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw}


def send_code(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    resp = send({"type": "execute_code", "params": {"code": code}})
    result = resp.get("result", resp)
    if isinstance(result, str) and len(result) > 2000:
        print(result[:2000])
        print("...[TRUNCADO]...")
    else:
        print(result)
    return resp


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(">>>", p)
        send_code(p)
