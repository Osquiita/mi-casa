# -*- coding: utf-8 -*-
"""
Generador Maestro del Archivo LayOut (.layout) para el proyecto 'mi-casa'.
Construye el paquete A3 completo de 12 láminas en formato nativo LayOut:
- Portada A3 Oficial
- Láminas P-00 a P-07 (Colección reglamentaria completa CTE)
- Láminas R-01 a R-03 (Renders 3D fotorrealistas de alta resolución)
"""

import os
import zipfile
import shutil
from pathlib import Path
import pymupdf  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
PLANOS_DIR = ROOT / "entrega" / "planos_2d"
RENDERS_DIR = ROOT / "entrega" / "renders"
OUTPUT_LAYOUT_DIR = ROOT / "entrega" / "planos"
OUTPUT_LAYOUT_DIR.mkdir(parents=True, exist_ok=True)

DESKTOP = Path(r"C:\Users\Oscar Martinez\Desktop")
LAYOUT_DESKTOP = DESKTOP / "00_PROYECTO_CASA_LAYOUT.layout"
LAYOUT_LOCAL = OUTPUT_LAYOUT_DIR / "00_PROYECTO_CASA_LAYOUT.layout"
LAYOUT_COMPLETO = OUTPUT_LAYOUT_DIR / "casa-bifamiliar-COMPLETO.layout"

# 1. Asegurar PNG de la Portada A3
portada_pdf = PLANOS_DIR / "00_portada_album_a3.pdf"
portada_png = PLANOS_DIR / "00_portada_album_a3.png"

if portada_pdf.exists():
    doc = pymupdf.open(str(portada_pdf))
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    pix.save(str(portada_png))
    doc.close()
    print(f"[OK] Portada A3 renderizada a PNG: {portada_png}")

# 2. Definición de Láminas
PAGES_CONFIG = [
    ("Portada Oficial A3", str(portada_png)),
    ("P-00: Emplazamiento y Justificación PGOU", str(PLANOS_DIR / "00_plano_emplazamiento_pgou.png")),
    ("P-01: Planta Baja Amueblada y Acotada", str(PLANOS_DIR / "01_plano_arquitecto_planta_baja.png")),
    ("P-02: Planta Alta Diáfana en Bruto", str(PLANOS_DIR / "02_plano_arquitecto_planta_alta_bruto.png")),
    ("P-03: Planta de Cubiertas e Instalaciones", str(PLANOS_DIR / "03_plano_cubiertas.png")),
    ("P-04: Alzados Exteriores Sur y Norte", str(PLANOS_DIR / "04_plano_alzados.png")),
    ("P-05: Secciones Constructivas A-A y B-B", str(PLANOS_DIR / "05_plano_secciones.png")),
    ("P-06: Estructura, Cimentación y Saneamiento", str(PLANOS_DIR / "06_plano_estructura.png")),
    ("P-07: Instalaciones Generales CTE", str(PLANOS_DIR / "07_plano_instalaciones.png")),
    ("R-01: Render 3D Fachada Principal Sur", str(RENDERS_DIR / "pro-fachada.png")),
    ("R-02: Render 3D Perspectiva Fachada Esquina", str(RENDERS_DIR / "pro-fachada2.png")),
    ("R-03: Render 3D Patio Central y Piscina", str(RENDERS_DIR / "pro-patios.png")),
    ("R-04: Render 3D Interior Salón y Cocina PB", str(RENDERS_DIR / "pro-interior-pb.png")),
    ("R-05: Render 3D Fachada Trasera Garaje", str(RENDERS_DIR / "pro-trasera.png")),
    ("R-06: Render 3D Axonometría Global", str(RENDERS_DIR / "pro-axo.png")),
]

def build_layout_file(dest_path):
    temp_zip = dest_path.with_suffix(".tmp.zip")
    
    PW = 16.535   # A3 = 420 mm en pulgadas
    PH = 11.693   # A3 = 297 mm en pulgadas
    M_LEFT = 0.20
    M_TOP = 0.20
    W_IMG = PW - 0.40
    H_IMG = PH - 0.40

    layer_id = "id12"
    
    with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        # Document Properties XML
        doc_props = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<documentProperties xmlns="http://sketchup.google.com/schemas/layout/1.0/documentproperties" xmlns:dp="http://sketchup.google.com/schemas/1.0/documentproperties" xmlns:r="http://sketchup.google.com/schemas/layout/1.0/references" xmlns:ldp="http://sketchup.google.com/schemas/layout/1.0/documentproperties" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://sketchup.google.com/schemas/layout/1.0/documentproperties http://sketchup.google.com/schemas/layout/1.0/documentproperties.xsd" generator="Antigravity Architect Pro" version="1.0"/>
"""
        z.writestr("documentProperties.xml", doc_props)

        # Style Manager XML
        style_mgr = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<styleManager xmlns="http://sketchup.google.com/schemas/1.0/preferences" xmlns:t="http://sketchup.google.com/schemas/1.0/types" xmlns:l="http://sketchup.google.com/schemas/layout/1.0/layout" xmlns:e="http://sketchup.google.com/schemas/layout/1.0/entities" xmlns:r="http://sketchup.google.com/schemas/layout/1.0/references" ver="1">
  <t:dicItem key="Default">
    <t:variant type="13">
      <e:styleAttributes>
        <t:dicItem key="stroke.pattern">
          <t:variant type="3" value="0"/>
        </t:dicItem>
      </e:styleAttributes>
    </t:variant>
  </t:dicItem>
</styleManager>
"""
        z.writestr("styleManager.xml", style_mgr)

        # Thumbnail (usar la portada)
        if portada_png.exists():
            z.write(str(portada_png), "doc_thumbnail.png")

        # Construir Páginas y Referencias
        ref_xml_lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>',
            '<references xmlns="http://sketchup.google.com/schemas/layout/1.0/references" xmlns:r="http://sketchup.google.com/schemas/layout/1.0/references" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" checkForUpdatesOnStartup="1" nextId="id999">'
        ]

        doc_page_refs = []
        
        for idx, (p_name, img_path) in enumerate(PAGES_CONFIG):
            p_num = idx + 1
            page_ref_id = f"id_pref_{p_num}"
            page_id = f"id_page_{p_num}"
            img_ref_id = f"id_iref_{p_num}"
            entity_id = f"id_ent_{p_num}"
            inst_id = f"id_inst_{p_num}"
            mgr_id = f"id_mgr_{p_num}"
            limgr_id = f"id_limgr_{p_num}"
            
            internal_img = f"ref/sheet_{p_num:02d}.png"
            if os.path.exists(img_path):
                z.write(img_path, internal_img)
            else:
                print(f"[WARN] No se encontró imagen: {img_path}")

            # Añadir referencias
            ref_xml_lines.append(f'  <r:pageFileReference r:id="{page_ref_id}" type="0" internalTarget="pages/page{p_num}.xml" externalTarget="" modificationDate="2026-10-18T00:00:00Z" insertDate="2026-10-18T00:00:00Z"/>')
            ref_xml_lines.append(f'  <r:imageFileReference r:id="{img_ref_id}" type="0" internalTarget="{internal_img}" externalTarget="{img_path.replace(os.sep, "/")}" modificationDate="2026-10-18T00:00:00Z" insertDate="2026-10-18T00:00:00Z"/>')

            # Document.xml page entry
            doc_page_refs.append(f'''    <ld:pageRef r:id="{page_ref_id}" id="{page_id}" name="{p_name}" showMasterLayers="1">
      <r:layerVisibility>1</r:layerVisibility>
    </ld:pageRef>''')

            # Escribir pages/pageN.xml
            page_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<page xmlns="http://sketchup.google.com/schemas/layout/1.0/page" id="{page_id}" xmlns:l="http://sketchup.google.com/schemas/layout/1.0/layout" xmlns:ld="http://sketchup.google.com/schemas/layout/1.0/layoutdocument" xmlns:r="http://sketchup.google.com/schemas/layout/1.0/references" xmlns:e="http://sketchup.google.com/schemas/layout/1.0/entities" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <layerEntityManager id="{mgr_id}">
    <entityList>
      <e:image id="{entity_id}">
        <e:placedFileReference>
          <e:rectangleBase x="{M_LEFT}" y="{M_TOP}" width="{W_IMG}" height="{H_IMG}">
            <e:graphicEntity shouldFill="0" shouldStroke="0">
              <e:entity/>
            </e:graphicEntity>
          </e:rectangleBase>
        </e:placedFileReference>
        <r:imageFileReference r:id="{img_ref_id}"/>
      </e:image>
    </entityList>
    <layerInstanceManager ver="2" id="{limgr_id}">
      <ld:layerInstance ver="2" id="{inst_id}">
        <ld:layerDefinition ver="2" l:ref="{layer_id}"/>
        <ld:entityList>
          <e:entity l:ref="{entity_id}"/>
        </ld:entityList>
      </ld:layerInstance>
    </layerInstanceManager>
  </layerEntityManager>
</page>
"""
            z.writestr(f"pages/page{p_num}.xml", page_content)

        ref_xml_lines.append('</references>')
        z.writestr("references.xml", "\n".join(ref_xml_lines))

        # Document XML
        page_refs_joined = "\n".join(doc_page_refs)
        doc_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<layoutDocument xmlns="http://sketchup.google.com/schemas/layout/1.0/layoutdocument" id="id_doc_main" xmlns:l="http://sketchup.google.com/schemas/layout/1.0/layout" xmlns:ld="http://sketchup.google.com/schemas/layout/1.0/layoutdocument" xmlns:r="http://sketchup.google.com/schemas/layout/1.0/references" xmlns:e="http://sketchup.google.com/schemas/layout/1.0/entities" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:n0="http://sketchup.google.com/schemas/layout/1.0/page">
  <ld:pageInfo id="id_pinfo" width="{PW}" height="{PH}" leftMargin="{M_LEFT}" rightMargin="{M_LEFT}" topMargin="{M_TOP}" bottomMargin="{M_TOP}" paperColor="4294967295" printPaper="0" showMargins="0" printMargins="0" marginColor="4278190335" targetDPI="300" editDrawingQuality="3" outputDrawingQuality="3" imageEditQuality="3" imageOutputQuality="3" editGroupDimLevel="0.66" editGroupHideOther="0"/>
  <ld:grid majorSpacing="1" minorDivisions="4" majorColor="4291480266" minorColor="2143996618" showGrid="0" showMinor="1" gridInFront="0" gridSnapTo="0" snapToMajor="0" snapToMinor="1" showMajor="1" printGrid="0" clipToMargins="0" gridType="0"/>
  <ld:unitsInfo format="3" unit="0" precision="6" suppressUnitDisplay="0" suppressDashesDisplay="0" forceInchDisplay="0" showFraction="0" suppressApproximateDisplay="0"/>
  <ld:layerManager id="id_layermgr">
    <ld:layerDefinition ver="2" id="{layer_id}" name="Plano_Principal" visible="1" locked="0" shared="0"/>
    <ld:currentLayerDefinition ver="2" l:ref="{layer_id}"/>
  </ld:layerManager>
  <n0:layerEntityManager id="id_n0lem">
    <n0:entityList/>
    <n0:layerInstanceManager ver="2" id="id_n0lim"/>
  </n0:layerEntityManager>
  <ld:pageManager id="id_pagemgr">
{page_refs_joined}
  </ld:pageManager>
  <ld:autoTextManager id="id_autotext">
    <ld:entityList>
      <ld:autoTextDefinition name="autor" type="3" textValue="Oscar Martinez"/>
      <ld:autoTextDefinition name="Company" type="3" textValue="Arquitectura y Promocion"/>
      <ld:autoTextDefinition name="Address" type="3" textValue="Calle Moreno Torroba s/n, Palma del Rio"/>
    </ld:entityList>
  </ld:autoTextManager>
  <n0:connectionManager/>
  <ld:lastPageDisplayed ver="1" l:ref="id_pref_1"/>
  <ld:objectSnapEnabled>1</ld:objectSnapEnabled>
</layoutDocument>
"""
        z.writestr("document.xml", doc_xml)

    # Reemplazar archivo destino
    if dest_path.exists():
        dest_path.unlink()
    shutil.move(str(temp_zip), str(dest_path))
    print(f"[EXITO] Documento LayOut generado: {dest_path} ({len(PAGES_CONFIG)} laminas)")

def export_layout_pdf():
    pdf_doc = pymupdf.open()
    rect_a3 = pymupdf.Rect(0, 0, 1190.52, 841.90)
    for p_name, img_path in PAGES_CONFIG:
        if os.path.exists(img_path):
            page = pdf_doc.new_page(width=1190.52, height=841.90)
            page.insert_image(rect_a3, filename=img_path)
    
    pdf_out1 = OUTPUT_LAYOUT_DIR / "00_CUADERNO_PLANOS_LAYOUT_A3.pdf"
    pdf_out2 = DESKTOP / "00_CUADERNO_PLANOS_LAYOUT_A3.pdf"
    pdf_doc.save(str(pdf_out1))
    pdf_doc.save(str(pdf_out2))
    pdf_doc.close()
    print(f"[EXITO] Cuaderno Completo PDF LayOut A3 generado: {pdf_out2}")

if __name__ == "__main__":
    build_layout_file(LAYOUT_LOCAL)
    build_layout_file(LAYOUT_DESKTOP)
    build_layout_file(LAYOUT_COMPLETO)
    export_layout_pdf()
    print("\nTODOS LOS ARCHIVOS LAYOUT Y PDF HAN SIDO ACTUALIZADOS AL 100%.")
