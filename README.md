# Proyecto Residencial Bifamiliar (Palma del Río, Córdoba)

> **Proyecto Básico y de Ejecución (PBE)** conforme a la **Ley 38/1999 (LOE)**, el **Código Técnico de la Edificación (CTE)** y el **PGOU del Ayuntamiento de Palma del Río**.  
> Edificación residencial entre medianeras en parcela pasante con dos viviendas independientes, patio central, piscina privada, porche, garaje con punto de recarga para vehículo eléctrico (Wallbox) y terrazas solárium.

---

## 🏛️ 1. Datos Generales del Proyecto

* **Tipología**: Residencial Bifamiliar entre medianeras (Vivienda A en Planta Baja y Vivienda B en Planta Alta).
* **Emplazamiento**: Calle Moreno Torroba s/n, 14700 Palma del Río (Córdoba).
* **Superficie de Parcela**: $205,90\text{ m}²$ ($11,60\text{ m}$ de fachada sur $\times 17,75\text{ m}$ de fondo pasante).
* **Superficie Construida Total**: **$351,40\text{ m}²$** ($196,80\text{ m}²$ en Planta Baja y $154,60\text{ m}²$ en Planta Alta).
* **Superficie Útil Cerrada**:
  * **Vivienda A (PB)**: $137,00\text{ m}²$ cerrados $+ 37,76\text{ m}²$ exteriores (porche cubierto y patio con piscina).
  * **Vivienda B (PA)**: $137,23\text{ m}²$ cerrados $+ 12,16\text{ m}²$ exterior (terraza solárium norte).
* **Altura**: 2 plantas sobre rasante ($B+1$) con $5,85\text{ m}$ de altura total a cornisa ($< 7,20\text{ m}$ permitidos por PGOU).
* **Eficiencia Energética**: Edificio de Consumo de Energía Casi Nulo (**nZEB**), bomba de calor aerotérmica para ACS y climatización por suelo radiante/refrescante ($>78\%$ renovable) y preinstalación de $4,5\text{ kWp}$ de energía solar fotovoltaica.

---

## 📁 2. Estructura del Repositorio

```
├── 📁 00_PROYECTO_FINAL_LICENCIA_AYUNTAMIENTO/     # Expediente oficial para Visado Colegial y Licencia Municipal
│   ├── 01_TOMO_I_MEMORIA_CTE_Y_ANEJOS.pdf         # Memoria Descriptiva, Constructiva, Justificación DBs, EBSS y Residuos
│   ├── 02_TOMO_II_ALBUM_PLANOS_REGLAMENTARIOS_A3.pdf # Colección completa de planos P-01 a P-07 a escala en DIN A3
│   ├── 03_TOMO_III_PLIEGO_DE_CONDICIONES.pdf      # Pliego de cláusulas administrativas y prescripciones técnicas
│   └── 04_TOMO_IV_MEDICIONES_Y_PRESUPUESTO.pdf    # Desglose en 17 capítulos PEM, PEC y liquidación de tasas ICIO
│
├── 📁 entrega/                                     # Documentación ejecutiva de entrega
│   ├── 📁 planos_2d/                              # Planos vectoriales en PDF y renders PNG a 300 DPI
│   │   ├── 01_plano_arquitecto_planta_baja.pdf / .png (P-01: PB amueblada y acotada 1:50)
│   │   ├── 02_plano_arquitecto_planta_alta.pdf / .png (P-02: PA Vivienda B amueblada y acotada 1:50)
│   │   ├── 03_plano_cubiertas.pdf / .png          (P-03: Cubiertas e Instalaciones Solares 1:100)
│   │   ├── 04_plano_alzados.pdf / .png            (P-04: Alzados Exteriores Sur y Norte 1:100)
│   │   ├── 05_plano_secciones.pdf / .png          (P-05: Secciones Constructivas Longitudinal y Transversal 1:75)
│   │   ├── 06_plano_estructura.pdf / .png         (P-06: Cimentación, Zapatas y Saneamiento 1:75)
│   │   └── 07_plano_instalaciones.pdf / .png      (P-07: Clima Aerotermia, VMC, Electricidad y Fontanería 1:75)
│   ├── 📁 planos/                                 # Archivos nativos de LayOut y SketchUp
│   │   ├── 00_PROYECTO_CASA_LAYOUT.layout
│   │   └── 00_CUADERNO_PLANOS_OFICIALES_A3.pdf
│   └── 📁 renders/                                # Renders fotorrealistas de alta resolución y perspectivas
│
├── 📁 tools/                                       # Scripts de automatización en Python y Ruby
│   ├── generar_plano_v6_perfeccionado.py          # Generador CAD Matplotlib de Planta Baja
│   ├── generar_plano_planta_alta_ejecutivo.py     # Generador CAD Matplotlib de Planta Alta
│   ├── generar_planos_tecnicos_completos.py       # Generador de P-03 a P-07
│   ├── generar_dossier_escrito_oficial.py         # Generador con fpdf2 de los Tomos I, III y IV del CTE
│   ├── inyectar_modelo_3d_bifamiliar_completo.rb  # Script Ruby para modelado paramétrico en SketchUp
│   └── reconstruir_layout_maestro.rb              # Script Ruby para ensamblado de láminas en LayOut
│
├── 🏠 casa-bifamiliar-3d.skp                       # Modelo 3D editable en SketchUp 2026
└── 📐 paso-01 a paso-05 (.dxf y .py)              # Geometría base y cuadros de superficies en formato DXF
```

---

## 🛠️ 3. Tecnologías y Formatos de Trabajo

* **Modelado 3D BIM y CAD**: Trimble SketchUp 2026, SketchUp LayOut 2026, Blender 3D.
* **Generación Técnica 2D**: Python 3.14 (`matplotlib`, `ezdxf`, `fpdf2`, `pypdf`, `pymupdf`).
* **Interoperabilidad**: Ruby API de SketchUp, DXF R2010, PDF vectorial y DIN A3 a escala oficial colegial.

---

## 📋 4. Justificación de los 4 Tomos Oficiales del CTE

1. **TOMO I: Memoria Técnica CTE y Anejos**:
   * Memoria Descriptiva y Urbanística (cumplimiento estricto del PGOU de Palma del Río).
   * Memoria Constructiva (zapatas HA-25, solera ventilada Cáviti, muros fónicos con lana de roca, carpinterías con RPT).
   * Justificación DB-SE, DB-SI, DB-SUA, DB-HE (nZEB), DB-HS (ventilación mecánica VMC continua) y DB-HR ($>50\text{ dBA}$).
   * Anejo de Seguridad y Salud (**EBSS**) y Estudio de Gestión de Residuos (**EGR** con fianza municipal).
2. **TOMO II: Álbum de Planos (A3)**:
   * 7 láminas ejecutivas normalizadas (P-01 a P-07) con cotas a 45º, grosores de muro y cajetín oficial.
3. **TOMO III: Pliego de Condiciones**:
   * Cláusulas administrativas bajo la Ley de Ordenación de la Edificación (LOE) y prescripciones técnicas de materiales.
4. **TOMO IV: Mediciones y Presupuesto**:
   * Desglose completo en 17 capítulos FIEBDC-3 (BC3).
   * **Presupuesto de Ejecución Material (P.E.M.)**: $279.800,00\text{ €}$.
   * **Presupuesto Base de Licitación / Contrata (P.E.C. con IVA)**: $366.258,20\text{ €}$.
   * **Liquidación Municipal**: Tasa de Licencia ($4.197,00\text{ €}$) $+$ ICIO 4% ($11.192,00\text{ €}$) $+$ Fianza Residuos ($1.500,00\text{ €}$) $=$ **$16.889,00\text{ €}$**.
