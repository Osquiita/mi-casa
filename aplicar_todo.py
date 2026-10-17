#!/usr/bin/env python3
"""
aplicar_todo.py — Instalador integral de mejoras para el proyecto 'mi-casa'.
Actualiza configuraciones, instala el servidor MCP, limpia duplicados y compila el proyecto.
"""

import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / "tools"
LEGACY = TOOLS / "legacy"
ENTREGA = ROOT / "entrega"

# 1. ACTUALIZACIÓN DE .gitignore
GITIGNORE_CONTENT = """# Python & Entornos Virtuales
__pycache__/
*.py[cod]
.venv/
venv/
.env

# Copias de seguridad de SketchUp, LayOut y Blender
*.skb
*.blend1
*.blend2
*~

# Artefactos temporales y volcados de depuración
tools/*_dump.txt
tools/legacy/
*.tmp
*.bak

# Binarios y ejecutables pesados (protección para GitHub)
*.zip
*.tar
*.gz
*.7z
tools/blender-5.2.0-windows-x64/
*.exe
*.dll
*.blend
*.exr
*.hdr
*.skp
*.layout
"""

# 2. ACTUALIZACIÓN DE opencode.json
OPENCODE_CONFIG = {
    "$schema": "https://opencode.ai/config.json",
    "mcp": {
        "arquitectura-mi-casa": {
            "type": "local",
            "command": [sys.executable, "tools/mcp_arquitectura_server.py"],
            "enabled": True,
            "environment": {
                "BLENDER_HOST": "127.0.0.1",
                "BLENDER_PORT": "9876",
                "SKETCHUP_HOST": "127.0.0.1",
                "SKETCHUP_PORT": "9877",
                "PYTHONPATH": "."
            }
        }
    }
}

# 3. PUENTE TRANSACCIONAL SKETCHUP / LAYOUT (tools/sketchup_bridge_pro.rb)
SKETCHUP_BRIDGE_RB = """# encoding: UTF-8
# tools/sketchup_bridge_pro.rb
# Ejecuta la construcción 3D, estilos, escenas y envío a LayOut en una operación atómica.

model = Sketchup.active_model
model.start_operation('Construccion_Maestra_Mi_Casa', true)

begin
  tools_dir = __dir__
  scripts = [
    'inyectar_modelo_3d_perfeccionado.rb',
    'apply_architect_style_sketchup.rb',
    'setup_escenas_completas_sketchup.rb',
    'save_for_layout.rb',
    'reconstruir_layout_maestro.rb'
  ]

  scripts.each do |script_name|
    full_path = File.join(tools_dir, script_name)
    if File.exist?(full_path)
      load full_path
    end
  end

  model.commit_operation
  puts "EXITO: Modelo 3D y LayOut sincronizados correctamente."
rescue => e
  model.abort_operation
  puts "ERROR EN PUENTE SKETCHUP: #{e.message}"
  puts e.backtrace.first(5).join("\\n")
end
"""

# 4. SERVIDOR MCP UNIFICADO (tools/mcp_arquitectura_server.py)
MCP_SERVER_PY = """#!/usr/bin/env python3
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

            sys.stdout.write(json.dumps(resp) + "\\n")
            sys.stdout.flush()
        except Exception as err:
            sys.stderr.write(f"Error MCP: {err}\\n")


if __name__ == "__main__":
    main()
"""

SCRIPTS_OBSOLETOS = [
    "probe_layout_api.rb", "probe_layout_api2.rb", "probe_ro.rb",
    "probe_styles.rb", "probe_table.rb", "test_text.rb",
    "check_send_param.rb", "check_send_to_layout.rb", "diag_3d.rb",
    "diagnostico_sketchup.rb", "sketchup_dump.txt",
    "sketchup_cambios_usuario_recientes.txt", "detalle_usuario.txt",
    "detalle_usuario.rb", "finish_v2.rb",
    "generar_plano_arquitecto_completo.py",
    "generar_plano_arquitecto_completo_con_muebles.py",
    "generar_plano_arquitecto_pulido.py",
    "generar_plano_pb_optimizado.py",
    "generar_plano_v6_perfeccionado.py",
    "build_contemporary_facade.py",
    "build_contemporary_no_trees.py",
    "build_3d.rb",
]

DUPLICADOS_RAIZ = [
    "paso-01-parcela.dxf", "paso-02-planta-baja.dxf", "paso-03-planta-alta.dxf",
    "paso-04-alzados-seccion.dxf", "paso-05-cuadro-superficies.dxf",
    "plano-01-parcela.pdf", "plano-02-planta-baja.pdf", "plano-03-planta-alta.pdf",
    "plano-04-alzados-seccion.pdf", "plano-05-cuadro-superficies.pdf",
]

PIPELINE_COMPILACION = [
    "paso_01_parcela.py",
    "paso_02_planta_baja.py",
    "paso_03_planta_alta.py",
    "paso_04_alzados_seccion.py",
    "paso_05_cuadro_superficies.py",
    "tools/generar_plano_v6_suite_optimizada.py",
    "tools/generar_plano_planta_alta_ejecutivo.py",
    "tools/generar_planos_tecnicos_completos.py",
    "tools/generar_dossier_escrito_oficial.py",
    "organizar_entrega.py",
    "tools/crear_zip_proyecto.py",
]


def ejecutar_instalacion():
    print("1/4 Escribiendo archivos de configuración y servidor MCP...")
    (ROOT / ".gitignore").write_text(GITIGNORE_CONTENT, encoding="utf-8")
    (ROOT / "opencode.json").write_text(json.dumps(OPENCODE_CONFIG, indent=2), encoding="utf-8")
    TOOLS.mkdir(parents=True, exist_ok=True)
    (TOOLS / "sketchup_bridge_pro.rb").write_text(SKETCHUP_BRIDGE_RB, encoding="utf-8")
    (TOOLS / "mcp_arquitectura_server.py").write_text(MCP_SERVER_PY, encoding="utf-8")

    print("2/4 Archivando scripts antiguos en tools/legacy/...")
    LEGACY.mkdir(parents=True, exist_ok=True)
    for item in SCRIPTS_OBSOLETOS:
        src = TOOLS / item
        if src.exists():
            shutil.move(str(src), str(LEGACY / item))

    print("3/4 Ejecutando pipeline de generación de planos, memorias y dossier...")
    for script in PIPELINE_COMPILACION:
        script_path = ROOT / script
        if script_path.exists():
            print(f"   -> Ejecutando {script}...")
            subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT))

    print("4/4 Limpiando artefactos duplicados de la raíz...")
    (ENTREGA / "planos").mkdir(parents=True, exist_ok=True)
    for dup in DUPLICADOS_RAIZ:
        dup_path = ROOT / dup
        if dup_path.exists():
            if dup.endswith(".dxf"):
                shutil.copy2(str(dup_path), str(ENTREGA / "planos" / dup))
            dup_path.unlink()

    print("\n¡PROYECTO MI-CASA 100% ACTUALIZADO, LIMPIO Y COMPILADO!")


if __name__ == "__main__":
    ejecutar_instalacion()
