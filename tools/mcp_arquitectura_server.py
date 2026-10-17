#!/usr/bin/env python3
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

BLENDER_HOST = os.getenv("BLENDER_HOST", "127.0.0.1")
BLENDER_PORT = int(os.getenv("BLENDER_PORT", "9876"))
SKETCHUP_HOST = os.getenv("SKETCHUP_HOST", "127.0.0.1")
SKETCHUP_PORT = int(os.getenv("SKETCHUP_PORT", "9877"))


def send_socket(host: str, port: int, payload: str, timeout: float = 45.0) -> str:
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.sendall(payload.encode("utf-8"))
        sock.shutdown(socket.SHUT_WR)
        chunks = []
        while True:
            data = sock.recv(65536)
            if not data:
                break
            chunks.append(data.decode("utf-8", errors="replace"))
        return "".join(chunks)


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "arquitectura-mi-casa", "version": "2.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "sincronizar_sketchup_y_layout",
                                "description": "Ejecuta sketchup_bridge_pro.rb en SketchUp y actualiza LayOut",
                                "inputSchema": {"type": "object", "properties": {}}
                            },
                            {
                                "name": "sincronizar_blender_3d",
                                "description": "Construye el proyecto maestro y materiales en Blender vía MCP",
                                "inputSchema": {"type": "object", "properties": {}}
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = req.get("params", {}).get("name")
                if name == "sincronizar_sketchup_y_layout":
                    rb_code = (ROOT_DIR / "tools" / "sketchup_bridge_pro.rb").read_text(encoding="utf-8")
                    out = send_socket(SKETCHUP_HOST, SKETCHUP_PORT, rb_code)
                elif name == "sincronizar_blender_3d":
                    py_code = (ROOT_DIR / "tools" / "build_master_complete_project.py").read_text(encoding="utf-8")
                    payload = json.dumps({"type": "execute_code", "params": {"code": py_code}})
                    out = send_socket(BLENDER_HOST, BLENDER_PORT, payload)
                else:
                    out = "Herramienta no reconocida"

                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": out}]}
                }
            else:
                continue

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as err:
            sys.stderr.write(f"Error MCP: {err}\n")


if __name__ == "__main__":
    main()
