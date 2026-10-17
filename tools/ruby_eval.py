# -*- coding: utf-8 -*-
"""Ejecuta codigo Ruby en SketchUp desde un archivo (o stdin) via sketchup_client."""
import sys
from sketchup_client import Client

if len(sys.argv) > 1:
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
else:
    code = sys.stdin.read()

c = Client()
try:
    c.connect()
    result = c.send("eval_ruby", {"code": code})
    print(result)
finally:
    c.close()