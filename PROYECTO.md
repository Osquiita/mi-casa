# Proyecto · Vivienda Bifamiliar en Palma del Río

Proyecto técnico completo de una **vivienda bifamiliar** en un solar entre medianeras de Palma del Río (Córdoba), desarrollado de forma programática: planos normativos en DXF/PDF, cuadro de superficies y presupuesto, y un **render 3D arquitectónico** profesional generado con Blender.

---

## 1. Datos del solar y normativa

| Parámetro | Valor |
|---|---|
| Solar | 11,40 × 17,60 m = **200 m²** |
| Forma | Entre medianeras, con fachada a dos calles (Moreno Torroba al frente, calle trasera al fondo) |
| Ocupación máxima | 80 % = **160 m²/planta** |
| Patio interior | 5,00 × 8,00 = **40 m²** (X 6,40–11,40 × Y 5,00–13,00), adosado al lindero derecho |
| Alturas | P.B. 0,22–2,90 m · P.A. 2,90–5,80 m · parapeto 6,10 m |

---

## 2. Programa

### Vivienda A — Planta baja (P-01)

| Estancia | Superficie |
|---|---|
| Salón-comedor (absorbe la antigua cocina) | 37,0 m² |
| Cocina (junto a escalera) | 20,0 m² |
| Baño + baño suite | 7,0 + 7,0 m² |
| Dormitorio principal (suite) | 14,0 m² |
| Dormitorio 2 | 11,2 m² |
| Dormitorio 3 | 11,2 m² |
| Trastero | 7,4 m² |
| Cochera (acceso a calle trasera) | 15,6 m² |
| Porche cubierto (X 6,40–11,40 × Y 5,00–7,60) | 13,0 m² |

**Claves de diseño (v6):**
- La antigua cocina se incorpora al **salón** (única pieza de 37 m²).
- Cocina junto a la escalera con **fontanería apilada** con P-02.
- Separación cocina-salón: **puerta corredera doble** (X 6,40, Y 1,00–4,40); abierta, todo el día queda unido.
- Cocina y salón abren al **porche cubierto** acristalado.
- Escalera recta (X 10,40–11,40 × Y 0–5,00, 17 escalones con descanso validado).
- **Ambos portales de 1,00 m** (portal A en X 0,30–1,30; portal B en X 10,40–11,40).

### Vivienda B — Planta alta (P-02, v8 confirmado)

| Estancia | Superficie |
|---|---|
| **Salón-comedor diáfano (integra el pasillo)** | **50,0 m²** |
| Cocina (junto a escalera) | 20,0 m² |
| Baño + baño suite | 7,0 + 7,0 m² |
| Dormitorio principal (suite) | 14,0 m² |
| **Dormitorio 2 al fondo-derecha (sobre cochera)** | **23,0 m²** |
| Dormitorio 3 | 11,2 m² |
| **Patio trasero elevado** (X 0–3,20 × Y 14,10–17,60) | **11,2 m²** |

**Claves de diseño (v8):**
- **Salón diáfano de 50 m²:** Se elimina la pared divisoria entre salón y pasillo en P.A., unificando todo el espacio frontal sobre el porche.
- **Sin escalera al tejado:** Acceso a cubierta no transitable (vía lucernario de registro sólo para mantenimiento), eliminando torres o módulos de escalera en tejado.
- **Fluidez visual y carpinterías continuas:** Huecos de puertas y ventanas totalmente diáfanos para máxima circulación de luz natural y vistas cruzadas.
- **Dormitorio 2 al fondo-derecha (23 m²)** sobre la cochera y **patio trasero elevado** (11,2 m²) privado.

---

## 3. Entregables generados

### Planos (DXF + PDF + preview PNG)
| Lámina | Archivo |
|---|---|
| P-00 · Parcela | `paso-01-parcela.dxf` / `plano-01-parcela.pdf` |
| P-01 · Planta baja (v6.1) | `paso-02-planta-baja.dxf` / `plano-02-planta-baja.pdf` |
| P-02 · Planta alta (v7) | `paso-03-planta-alta.dxf` / `plano-03-planta-alta.pdf` |
| P-03/P-04 · Alzados y sección | `paso-04-alzados-seccion.dxf` / `plano-04-alzados-seccion.pdf` |
| P-05 · Cuadro de superficies y presupuesto (≈ **381.000 €**) | `paso-05-cuadro-superficies.dxf` / `plano-05-cuadro-superficies.pdf` |
| **Documento único completo** | **`proyecto-completo.pdf`** (P-00…P-05, 5 páginas) |

### Modelo y render 3D
| Recurso | Archivo |
|---|---|
| Modelo completo Blender | `casa-bifamiliar-3d.blend` (**469 objetos**) |
| Fachada frontal (nivel de ojo, 35 mm) | `pro-fachada.png` |
| Fachada frontal alternativa (32 mm) | `pro-fachada2.png` |
| Alzado trasero (nivel de ojo) | `pro-trasera.png` |
| Vista axonométrica | `pro-axo.png` |
| Patios y porche | `pro-patios.png` |
| Interior planta baja | `pro-interior-pb.png` |
| Interior planta alta | `pro-interior-pa.png` |

*(Renders 2560 × 1440 px, motor **EEVEE** — el hardware AMD iGPU no rinde con Cycles.)*

---

## 4. Proceso de trabajo

1. **Diseño y validación geométrica** en Python con coordenadas reales en metros (`plan_data.py` + scripts `paso_01…05`), generando DXF con ezdxf y PDF/PNG.
2. **Exportación PDF** individual por lámina y **PDF único** `proyecto-completo.pdf`.
3. **Render 3D**: se evaluó SketchUp (no instalado) → se eligió **Blender + BlenderMCP**:
   - Blender **5.2.0 LTS portable** + addon BlenderMCP (servidor TCP 9876) + MCP configurado en `opencode.json`.
   - Construcción programática del modelo con **469 objetos**: muros, forjados, escalera, mobiliario completo, vegetación, entorno urbanizado y coche en la cochera.
   - **Cielo realista** (Sky HOSEK_WILKIE) + sol cálido, **materiales PBR** procedurales (estuco, hormigón, madera, vidrio, asfalto, césped), iluminación interior y cámaras arquitectónicas a nivel de ojo.
4. **Limpieza final**: se conservaron únicamente planos aprobados, PDF, modelo y renders válidos; se eliminaron versiones antiguas.

---

## 5. Estructura de archivos

```
mi-casa/
├── proyecto-completo.pdf        # Documento único (P-00…P-05)
├── casa-bifamiliar-3d.blend     # Modelo 3D completo
├── pro-*.png                    # 7 renders arquitectónicos
├── paso_01_parcela.py …         # Scripts generadores de planos
├── paso-01…05-*.dxf             # Planos en DXF
├── plano-01…05-*.pdf            # Planos en PDF
├── preview-01…05-*.png          # Vistas previas de planos
├── plan_data.py                 # Datos geométricos compartidos
├── exportar_pdf*.py             # Exportadores de PDF
└── tools/
    ├── blender.zip              # Blender 5.2 portable
    ├── BlenderMCP_addon.py      # Addon servidor BlenderMCP
    ├── blender_client.py        # Cliente socket (puerto 9876)
    ├── blender_lib.py           # Librería de primitivas 3D
    ├── blender_pro_build.py     # Construcción del modelo (469 objetos)
    └── blender_pro_render.py    # Render EEVEE de las 7 vistas
```

---

## 6. Cómo regenerar todo

```powershell
# Planos y PDFs
python paso_01_parcela.py && python paso_02_planta_baja.py && python paso_03_planta_alta.py
python paso_04_alzados_seccion.py && python paso_05_cuadro_superficies.py
python exportar_pdf_completo.py

# Render 3D (requiere Blender abierto con el addon BlenderMCP activo)
python tools\blender_pro_build.py
python tools\blender_pro_render.py
```

> Nota: el modelo no es capaz de ver las imágenes; toda la geometría se reconstruye a partir de scripts para garantizar exactitud dimensional.
