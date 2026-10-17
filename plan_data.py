# -*- coding: utf-8 -*-
"""Datos geometricos compartidos del proyecto. Unidades: metros."""
import math

# --- parcela
X0, Y0 = 0.0, 0.0
X1, Y1 = 11.40, 17.60          # solar 11,40 x 17,60 m = 200 m²

# --- patio: 40 m² adosado a lindero derecho, banda central.
# Ancho 5,00 x Fondo 8,00 = 40 m² (optimizado para el resto de la casa)
P_W, P_D = 5.00, 8.00
PX0 = X1 - P_W                  # 6.40
PY0 = 5.00
PX1 = X1                        # 11.40
PY1 = PY0 + P_D                 # 13.00

# --- bandas
FRONT_D = PY0 - Y0              # 5.00  (zona dia + escalera)
REAR_D = Y1 - PY1               # 4.60  (cochera + dormitorios a calle trasera)
LEFT_W = PX0 - X0               # 6.40  (columna izquierda: cocina + dorm ppal + distribuidor)

# --- escalera recta Vivienda B (hueco 1,40 x 5,90)
ST_W, ST_D = 1.40, 5.90
ST_X0, ST_Y0 = X0, Y0           # esquina izq-frente
ST_X1, ST_Y1 = ST_X0 + ST_W, ST_Y0 + ST_D

# --- cochera (acceso calle trasera)
G_W, G_D = 3.40, REAR_D
G_X0 = X1 - G_W                 # 8.00
G_Y0 = PY1
G_X1, G_Y1 = X1, Y1

# --- bandas de habitaciones en franja trasera
DORM_BAND_X0 = X0               # 0.00
DORM_BAND_X1 = G_X0             # 8.00

def area(w, d):
    return w * d

if __name__ == "__main__":
    print(f"Solar: {X1-X0:.2f} x {Y1-Y0:.2f} = {(X1-X0)*(Y1-Y0):.0f} m2")
    print(f"Patio: {P_W:.2f} x {P_D:.2f} = {area(P_W,P_D):.0f} m2")
    print(f"Huella edificable: {200-area(P_W,P_D):.0f} m2/planta (80%)")
    print(f"Banda frontal {FRONT_D:.2f} | columna izq {LEFT_W:.2f} | banda trasera {REAR_D:.2f}")
