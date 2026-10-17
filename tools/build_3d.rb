# -*- coding: utf-8 -*-
# Build 3D completo v2 - Casa bifamiliar Palma del Rio (SketchUp, mm).
# Geometria corregida: z_f=0.22, forjado 0.20, z_ha=5.80, parapeto 6.12.
# Incluye: entorno, mobiliario, vegetacion, coche, pergola, barandillas.

M = 1000.0
ZF = 0.22; ZHB = 2.90; ZPA = 2.90; ZHA = 5.80
RF_B = ZHA; RF_T = ZHA + 0.20; PARA_T = ZHA + 0.32; ALB_T = ZHA + 0.35
V_ALF = 0.90; V_TOP = 2.40; D_TOP = 2.10

MODEL = Sketchup.active_model; ENTS = MODEL.entities; LAYS = MODEL.layers

def mm(v) v * M; end

def box(x1,y1,z1,x2,y2,z2,name,layer=nil)
  g = ENTS.add_group; g.name = name
  g.layer = LAYS[layer] if layer && LAYS[layer]
  es = g.entities
  f = es.add_face([Geom::Point3d.new(mm(x1),mm(y1),mm(z1)),Geom::Point3d.new(mm(x2),mm(y1),mm(z1)),
    Geom::Point3d.new(mm(x2),mm(y2),mm(z1)),Geom::Point3d.new(mm(x1),mm(y2),mm(z1))])
  f.reverse! if f.normal.z < 0; f.pushpull(mm(z2-z1)); g
end

def clip(a,b,gaps)
  pts=([a,b]+gaps.flatten.select{|p|p>a&&p<b}).sort.uniq; segs=[]
  (0...(pts.size-1)).each{|i|p=pts[i];q=pts[i+1];next if gaps.any?{|g|g[0]<=p&&q<=g[1]};segs<<[p,q] if q-p>1e-6}; segs
end

def build_wall_h(y,x0,x1,openings,t,z0,z1,name,layer="MUROS")
  gaps=openings.map{|o|o[0..1]}; i=0
  clip(x0,x1,gaps).each{|(a,b)|box(a,y-t/2.0,z0,b,y+t/2.0,z1,"#{name}-s#{i}",layer);i+=1}
  openings.each_with_index{|(a,b,tipo),j|
    case tipo
    when :puerta then box(a,y-t/2.0,D_TOP,b,y+t/2.0,z1,"#{name}-d#{j}",layer)
    when :ventana
      box(a,y-t/2.0,z0,b,y+t/2.0,V_ALF,"#{name}-w-alf#{j}",layer)
      box(a,y-t/2.0,V_TOP,b,y+t/2.0,z1,"#{name}-w-din#{j}",layer)
    when :ventanal
      # hueco completo de suelo a techo (sin alféizar ni dintel)
    end}
end

def build_wall_v(x,y0,y1,openings,t,z0,z1,name,layer="MUROS")
  gaps=openings.map{|o|o[0..1]}; i=0
  clip(y0,y1,gaps).each{|(a,b)|box(x-t/2.0,a,z0,x+t/2.0,b,z1,"#{name}-s#{i}",layer);i+=1}
  openings.each_with_index{|(a,b,tipo),j|
    case tipo
    when :puerta then box(x-t/2.0,a,D_TOP,x+t/2.0,b,z1,"#{name}-d#{j}",layer)
    when :ventana
      box(x-t/2.0,a,z0,x+t/2.0,b,V_ALF,"#{name}-w-alf#{j}",layer)
      box(x-t/2.0,a,V_TOP,x+t/2.0,b,z1,"#{name}-w-din#{j}",layer)
    when :ventanal
      # hueco completo de suelo a techo
    end}
end

def glazing_h(y,a,b,t,z0,z1,name)
  g=ENTS.add_group;g.name=name;g.layer=LAYS["VENTANAS"] if LAYS["VENTANAS"];es=g.entities
  f=es.add_face([Geom::Point3d.new(mm(a),mm(y),mm(z0)),Geom::Point3d.new(mm(b),mm(y),mm(z0)),
    Geom::Point3d.new(mm(b),mm(y),mm(z1)),Geom::Point3d.new(mm(a),mm(y),mm(z1))])
  f.reverse! if f.normal.x<0;f.pushpull(mm(t));g
end

def glazing_v(x,a,b,t,z0,z1,name)
  g=ENTS.add_group;g.name=name;g.layer=LAYS["VENTANAS"] if LAYS["VENTANAS"];es=g.entities
  f=es.add_face([Geom::Point3d.new(mm(x),mm(a),mm(z0)),Geom::Point3d.new(mm(x),mm(b),mm(z0)),
    Geom::Point3d.new(mm(x),mm(b),mm(z1)),Geom::Point3d.new(mm(x),mm(a),mm(z1))])
  f.reverse! if f.normal.y<0;f.pushpull(mm(t));g
end

def oct_cylinder(name,cx,cy,r,z0,z1,layer)
  g=ENTS.add_group;g.name=name;g.layer=LAYS[layer] if layer&&LAYS[layer];es=g.entities
  n=8;pts=(0...n).map{|i|a=2*Math::PI*i/n;Geom::Point3d.new(mm(cx+r*Math.cos(a)),mm(cy+r*Math.sin(a)),mm(z0))}
  f=es.add_face(pts);f.reverse! if f.normal.z<0;f.pushpull(mm(z1-z0));g
end

# ================================================================ LIMPIEZA
ENTS.clear!

# ================================================================ FASE 1: ENTORNO
box(-4.0,-12.0,0.0, 14.4,-1.2,0.16, "calle-frente","PARCELA")
box(-3.0,-1.2,0.0, 14.4,0.0,0.12, "acera-frente","PARCELA")
box(-4.0,17.6,0.0, 14.4,28.0,0.16, "calle-trasera","PARCELA")
box(-3.0,17.6,0.0, 14.4,18.8,0.12, "acera-trasera","PARCELA")
box(-3.0,-1.2,0.0, 0.0,17.6,0.12, "acera-izq","PARCELA")
box(11.4,-1.2,0.0, 14.4,17.6,0.12, "acera-der","PARCELA")
box(-3.0,0.0,-0.06, 14.4,17.6,0.0, "ground-plot","PARCELA")

# cesped
box(-3.0,-1.2,0.02, 0.0,0.0,0.06, "cesped-frente","PARCELA")
box(0.0,17.6,0.02, 3.2,18.8,0.06, "cesped-tras","PARCELA")
box(-0.2,0.0,0.02, 0.0,17.6,0.06, "cesped-medianera-l","PARCELA")
box(11.4,0.0,0.02, 11.6,17.6,0.06, "cesped-medianera-r","PARCELA")

# setos
box(-2.5,-0.35,0.0, 0.0,-0.15,1.0, "seto-frente","PARCELA")
box(-2.9,-0.2,0.0, -2.7,3.0,1.1, "seto-lateral","PARCELA")

# ================================================================ FASE 2: SOLERA + P.B.
box(0.0,0.0,0.15, 11.40,17.60,0.22, "slab-pb","MUROS")

# envolvente P.B.
build_wall_v(0.0,0.0,17.60,[],0.30,ZF,ZHB,"med-izq")
build_wall_v(11.40,0.0,17.60,[[2.80,3.60,:ventana]],0.30,ZF,ZHB,"med-der")
build_wall_h(0.0,0.0,11.40,
  [[0.30,1.30,:puerta],[2.60,4.40,:ventanal],[4.80,6.00,:ventanal],
   [6.90,8.10,:ventana],[8.90,9.90,:ventana],[10.40,11.40,:puerta]],
  0.30,ZF,ZHB,"fach-frontal")
build_wall_h(17.60,0.0,11.40,
  [[0.80,2.40,:ventana],[3.60,5.20,:ventana],[8.60,11.00,:vacio]],
  0.30,ZF,ZHB,"fach-trasera")

# interiores P.B.
build_wall_v(1.40,0.0,13.00,[[1.40,4.60,:puerta],[7.90,8.60,:puerta]],0.10,ZF,ZHB,"t-pasillo","TABIQUES")
build_wall_v(6.40,0.0,5.00,[[1.00,4.40,:vacio]],0.10,ZF,ZHB,"t-corredera","TABIQUES")
build_wall_v(6.40,5.00,7.40,[[5.30,6.20,:puerta]],0.30,ZF,ZHB,"m-salporche")
build_wall_v(6.40,7.40,13.00,[[7.80,8.40,:ventana],[9.00,9.60,:ventana],[11.00,12.20,:ventana]],0.30,ZF,ZHB,"m-patio")
build_wall_v(10.40,0.0,5.00,[],0.15,ZF,ZHB,"m-caja-esc")
build_wall_h(5.00,6.40,11.40,[[6.40,10.40,:vacio]],0.30,ZF,ZHB,"m-coccier")
build_wall_h(7.40,1.40,6.40,[],0.10,ZF,ZHB,"t-banoA","TABIQUES")
build_wall_h(8.80,1.40,6.40,[],0.10,ZF,ZHB,"t-banoB","TABIQUES")
build_wall_h(10.20,1.40,6.40,[[3.30,4.00,:puerta]],0.10,ZF,ZHB,"t-dorm","TABIQUES")
build_wall_h(13.00,1.40,8.00,[[2.20,2.90,:puerta]],0.10,ZF,ZHB,"t-nido","TABIQUES")
build_wall_v(4.50,13.00,14.10,[],0.10,ZF,ZHB,"t-vestidor","TABIQUES")
build_wall_h(14.10,0.0,4.50,[[0.80,1.50,:puerta],[3.60,4.30,:puerta]],0.10,ZF,ZHB,"t-norte","TABIQUES")
build_wall_v(6.40,13.00,17.60,[],0.10,ZF,ZHB,"t-trasero","TABIQUES")
build_wall_v(8.00,13.00,17.60,[[13.30,13.90,:puerta]],0.15,ZF,ZHB,"m-trast-cochera")
build_wall_v(3.20,14.10,17.60,[],0.10,ZF,ZHB,"t-dorm-dorm","TABIQUES")

# columnas porche
[[7.00,7.50],[9.60,7.50]].each_with_index{|(cx,cy),k|
  box(cx-0.10,cy-0.10,ZF,cx+0.10,cy+0.10,RF_B,"col-porche#{k}","MUROS")}

# escalera con meseta de acceso (no empieza en la puerta)
H_R = (ZHB-ZF)/17.0     # ≈0.158 contraste
LND = 1.0               # profundidad meseta
box(10.45,0.0,ZF, 11.35,LND,ZF+H_R, "esc-meseta","ESCALERA")
tread = (5.0-LND)/16.0  # ≈0.25 huella
16.times{|i|
  y0=LND+i*tread;y1=y0+tread;z1=ZF+(i+2)*H_R
  box(10.45,y0,ZF,11.35,y1,z1,"esc-#{i}","ESCALERA")}

# ================================================================ FASE 3: FORJADO P.A.
box(0.0,0.0,ZHB, 11.40,5.00,ZHB+0.20, "fj-front","MUROS")
box(0.0,5.00,ZHB, 6.40,17.60,ZHB+0.20, "fj-west","MUROS")
box(6.40,5.00,ZHB, 11.40,7.60,ZHB+0.20, "fj-pas","MUROS")
box(6.40,13.00,ZHB, 11.40,17.60,ZHB+0.20, "fj-d2","MUROS")

# ================================================================ FASE 4: MUROS P.A.
build_wall_v(0.0,0.0,17.60,[],0.30,ZPA,ZHA,"med-izq-PA")
build_wall_v(11.40,0.0,17.60,[[2.80,3.60,:ventana]],0.30,ZPA,ZHA,"med-der-PA")
build_wall_h(0.0,0.0,11.40,
  [[2.60,4.40,:ventanal],[4.80,6.00,:ventanal],[6.90,8.10,:ventana],[8.90,9.90,:ventana]],
  0.30,ZPA,ZHA,"fach-front-PA")
build_wall_h(17.60,0.0,11.40,
  [[3.60,5.20,:ventana],[7.00,9.00,:ventana],[9.80,11.20,:ventana]],
  0.30,ZPA,ZHA,"fach-tras-PA")
build_wall_v(10.40,0.0,5.00,[],0.15,ZPA,ZHA,"m-caja-esc-PA")
build_wall_v(6.40,7.60,13.00,[[7.80,8.40,:ventana],[9.00,9.60,:ventana],[11.00,12.20,:ventana]],0.30,ZPA,ZHA,"m-patio-PA")
build_wall_v(1.40,0.0,5.00,[[1.00,4.40,:vacio]],0.10,ZPA,ZHA,"t-corr-PA","TABIQUES")
build_wall_v(1.40,5.00,13.00,[[7.90,8.60,:puerta]],0.10,ZPA,ZHA,"t-paso-PA","TABIQUES")
build_wall_h(7.40,1.40,6.40,[],0.10,ZPA,ZHA,"t-bA-PA","TABIQUES")
build_wall_h(8.80,1.40,6.40,[],0.10,ZPA,ZHA,"t-bB-PA","TABIQUES")
build_wall_h(10.20,1.40,6.40,[[3.30,4.00,:puerta]],0.10,ZPA,ZHA,"t-dorm-PA","TABIQUES")
build_wall_h(13.00,1.40,6.40,[[2.20,2.90,:puerta]],0.10,ZPA,ZHA,"t-dist-PA","TABIQUES")
build_wall_h(14.10,0.0,6.40,[[0.80,1.50,:puerta],[3.60,4.30,:puerta]],0.10,ZPA,ZHA,"t-norte-PA","TABIQUES")
build_wall_v(6.40,13.00,17.60,[[13.20,14.00,:puerta]],0.10,ZPA,ZHA,"t-d2-PA","TABIQUES")
build_wall_v(3.20,14.10,17.60,[],0.10,ZPA,ZHA,"t-jardin-PA","TABIQUES")
build_wall_h(13.00,6.40,11.40,[[7.00,10.40,:ventana]],0.10,ZPA,ZHA,"t-d2sur-PA","TABIQUES")

# ================================================================ FASE 5: CUBIERTA + PARAPETO + ALBARDILLAS
box(0.0,0.0,RF_B, 11.40,17.60,RF_T, "cubierta","MUROS")
# parapetos perimetrales
box(-0.15,-0.15,RF_B, 11.55,0.15,PARA_T, "parap-n","MUROS")
box(-0.15,17.45,RF_B, 11.55,17.75,PARA_T, "parap-s","MUROS")
box(-0.15,-0.15,RF_B, 0.15,17.75,PARA_T, "parap-o","MUROS")
box(11.25,-0.15,RF_B, 11.55,17.75,PARA_T, "parap-e","MUROS")
# albardillas metalicas
box(-0.05,-0.18,PARA_T, 11.45,0.18,ALB_T, "alb-n","METAL")
box(-0.05,17.42,PARA_T, 11.45,17.78,ALB_T, "alb-s","METAL")
box(-0.18,-0.05,PARA_T, 0.18,17.65,ALB_T, "alb-o","METAL")
box(11.22,-0.05,PARA_T, 11.58,17.65,ALB_T, "alb-e","METAL")

# ================================================================ FASE 6: PERGOLA + BARANDILLAS + LAMAS
# pergola bioclimatica en patio (X 6.30-11.50, Y 5.00-12.80, z 2.58-2.82)
12.times{|i|py=5.2+i*0.65; box(6.30,py-0.04,2.70, 11.50,py+0.04,2.82, "pergola-lama#{i}","WOOD")}
box(6.35,5.00,2.58, 6.45,12.80,2.70, "pergola-viga-l","WOOD")
box(11.35,5.00,2.58, 11.45,12.80,2.70, "pergola-viga-r","WOOD")

# barandilla balcón sobre porche (X 6.40-11.40, Y 7.60, z 3.10-4.00)
BZ0 = ZHB + 0.20   # 3.10 suelo balcón
BZ1 = BZ0 + 0.90   # 4.00 pasamanos
box(6.40,7.55,BZ0, 11.40,7.65,0.06, "balc-cintura","METAL")
box(6.35,7.55,BZ0, 11.45,7.65,BZ1, "balc-pasa","METAL")
16.times{|i| bx = 6.45 + i*(4.90/15.0); box(bx-0.015,7.55,BZ0+0.06, bx+0.015,7.65,BZ1, "balc-bar{#{i}}","METAL")}

# barandilla patio trasero elevado (X 3.08-3.20, Y 14.22-17.48, z 2.96-3.30)
box(3.08,14.22,2.96, 3.20,17.48,3.30, "barandilla-d2","METAL")
box(0.0,14.10,2.90, 0.12,17.60,3.20, "parap-pat2-o","MUROS")
box(0.0,17.48,2.90, 3.20,17.60,3.20, "parap-pat2-n","MUROS")
box(0.0,14.10,2.90, 3.20,14.22,3.20, "parap-pat2-s","MUROS")

# lamas decorativas fachada (X 1.6-2.5, Y -0.10, z 0.2-2.8)
8.times{|j|lx=1.6+j*0.12; box(lx-0.02,-0.10,0.2, lx+0.02,-0.02,2.8, "lama-fachada#{j}","WOOD")}

# suelo patio central (bajo porche)
box(6.40,5.00,0.0, 11.40,13.00,0.06, "pav-patio","MUROS")

# suelo patio trasero elevado
box(0.0,14.10,2.90, 3.20,17.60,2.96, "pav-pat2","MUROS")

# ================================================================ FASE 7: PUERTAS
# Portal A (Y=0, X 0.30-1.30)
box(0.30,-0.07,ZF, 1.30,0.07,ZF+D_TOP, "puerta-portalA","WOOD")
# Portal B (Y=0, X 10.40-11.40)
box(10.40,-0.07,ZF, 11.40,0.07,ZF+D_TOP, "puerta-portalB","WOOD")
# Salon->porche (X=6.40, Y 5.30-6.20)
box(6.33,5.30,ZF, 6.47,6.20,ZF+D_TOP, "puerta-salpor","WOOD")
# Banio comun (X=1.40, Y 7.90-8.60)
box(1.33,7.90,ZF, 1.47,8.60,ZF+D_TOP, "puerta-bano","WOOD")
# Suite (Y=10.20, X 3.30-4.00)
box(3.30,10.13,ZF, 4.00,10.27,ZF+D_TOP, "puerta-suite","WOOD")
# Dorm principal (Y=13.00, X 2.20-2.90)
box(2.20,12.93,ZF, 2.90,13.07,ZF+D_TOP, "puerta-dppal","WOOD")
# Dorm2 (Y=14.10, X 0.80-1.50)
box(0.80,14.03,ZF, 1.50,14.17,ZF+D_TOP, "puerta-dorm2","WOOD")
# Dorm3 (Y=14.10, X 3.60-4.30)
box(3.60,14.03,ZF, 4.30,14.17,ZF+D_TOP, "puerta-dorm3","WOOD")
# Trastero (X=8.00, Y 13.30-13.90)
box(7.93,13.30,ZF, 8.07,13.90,ZF+D_TOP, "puerta-trastero","WOOD")
# Porton cochera (Y=17.60, X 8.60-11.00)
box(8.60,17.53,ZF, 11.00,17.67,ZF+2.40, "porton-cochera","GARAGE")
# Corredera doble salon-cocina (X=6.40, Y 1.00-4.40)
box(6.33,1.00,ZF, 6.47,4.40,ZF+2.60, "corredera-salcoc","WOOD")
# Puertas P.A. (mismas posiciones, z=ZPA)
box(0.30,-0.07,ZPA, 1.30,0.07,ZPA+D_TOP, "puerta-portalA-PA","WOOD")
box(10.40,-0.07,ZPA, 11.40,0.07,ZPA+D_TOP, "puerta-portalB-PA","WOOD")
box(6.33,5.30,ZPA, 6.47,6.20,ZPA+D_TOP, "puerta-salpor-PA","WOOD")
box(1.33,7.90,ZPA, 1.47,8.60,ZPA+D_TOP, "puerta-bano-PA","WOOD")
box(3.30,10.13,ZPA, 4.00,10.27,ZPA+D_TOP, "puerta-suite-PA","WOOD")
box(2.20,12.93,ZPA, 2.90,13.07,ZPA+D_TOP, "puerta-dppal-PA","WOOD")
box(0.80,14.03,ZPA, 1.50,14.17,ZPA+D_TOP, "puerta-dorm2-PA","WOOD")
box(3.60,14.03,ZPA, 4.30,14.17,ZPA+D_TOP, "puerta-dorm3-PA","WOOD")
box(13.13,13.20,ZPA, 13.27,14.00,ZPA+D_TOP, "puerta-d2-PA","WOOD")
box(6.33,1.00,ZPA, 6.47,4.40,ZPA+2.60, "corredera-PA","WOOD")

# ================================================================ FASE 8: VIDRIOS
[[2.60,4.40],[4.80,6.00],[6.90,8.10],[8.90,9.90]].each_with_index{|(a,b),i|
  glazing_h(0.025,a,b,0.05,V_ALF,V_TOP,"crist-f-pb#{i}")}
[[0.80,2.40],[3.60,5.20]].each_with_index{|(a,b),i|
  glazing_h(17.575,a,b,0.05,V_ALF,V_TOP,"crist-t-pb#{i}")}
glazing_v(11.375,2.80,3.60,0.05,V_ALF,V_TOP,"crist-esc-pb")
[[2.60,4.40],[4.80,6.00],[6.90,8.10],[8.90,9.90]].each_with_index{|(a,b),i|
  glazing_h(0.025,a,b,0.05,ZPA+V_ALF,ZPA+V_TOP,"crist-f-pa#{i}")}
[[3.60,5.20],[7.00,9.00],[9.80,11.20]].each_with_index{|(a,b),i|
  glazing_h(17.575,a,b,0.05,ZPA+V_ALF,ZPA+V_TOP,"crist-t-pa#{i}")}
glazing_v(11.375,2.80,3.60,0.05,ZPA+V_ALF,ZPA+V_TOP,"crist-esc-pa")
[[7.80,8.40],[9.00,9.60],[11.00,12.20]].each_with_index{|(a,b),i|
  glazing_v(6.425,a,b,0.05,V_ALF,V_TOP,"crist-p-pb#{i}")
  glazing_v(6.425,a,b,0.05,ZPA+V_ALF,ZPA+V_TOP,"crist-p-pa#{i}")}
glazing_h(13.025,7.00,10.40,0.05,ZPA+V_ALF,ZPA+V_TOP,"crist-d2sur-pa")
glazing_h(4.975,6.40,10.40,0.05,ZF,ZHB,"crist-coc-porche")

# ================================================================ FASE 9: MOBILIARIO P.B.
# salon
box(2.00,2.40,ZF, 5.00,3.10,ZF+0.70, "sofa-pb","MOBILIARIO")
box(2.40,4.60,ZF, 4.00,6.20,ZF+0.75, "mesa-com-pb","MOBILIARIO")
box(2.60,6.98,ZF+0.90, 4.20,7.32,ZF+1.80, "tv-pb","MOBILIARIO")
box(1.60,0.30,ZF, 2.20,0.90,ZF+0.45, "butaca-pb","MOBILIARIO")
# cocina
box(6.55,4.55,ZF, 10.25,4.90,ZF+0.92, "encim-s-pb","MOBILIARIO")
box(10.05,0.60,ZF, 10.35,4.50,ZF+0.92, "encim-e-pb","MOBILIARIO")
box(7.60,2.20,ZF, 9.20,2.70,ZF+0.92, "isla-pb","MOBILIARIO")
box(7.55,2.15,ZF+0.92, 9.25,2.75,ZF+0.96, "isla-top-pb","MOBILIARIO")
box(9.55,0.40,ZF, 10.00,1.10,ZF+1.80, "frigo-pb","MOBILIARIO")
# porche
box(7.00,6.30,ZF, 8.60,6.90,ZF+0.75, "mesa-porche","MOBILIARIO")
# banos
box(1.60,7.45,ZF, 3.60,7.80,ZF+0.85, "lavabo-bano","MOBILIARIO")
box(2.20,8.05,ZF, 2.60,8.75,ZF+0.40, "wc-bano","MOBILIARIO")
box(5.50,7.55,ZF, 6.40,8.65,ZF+2.00, "ducha-bano","MOBILIARIO")
box(1.60,8.85,ZF, 3.60,9.20,ZF+0.85, "lavabo-suite","MOBILIARIO")
box(2.20,9.40,ZF, 2.60,10.10,ZF+0.40, "wc-suite","MOBILIARIO")
box(5.50,8.95,ZF, 6.40,10.05,ZF+2.00, "ducha-suite","MOBILIARIO")
# dorm principal
box(4.00,11.00,ZF, 5.80,13.00,ZF+0.50, "cama-dppal","MOBILIARIO")
box(4.00,11.00,ZF+0.50, 5.80,11.20,ZF+1.20, "cab-cppal","MOBILIARIO")
box(1.55,10.80,ZF, 2.05,12.60,ZF+2.30, "arm-dppal","MOBILIARIO")
# dorm2
box(0.15,15.30,ZF, 1.65,17.30,ZF+0.50, "cama-d2","MOBILIARIO")
box(0.15,15.30,ZF+0.50, 1.65,15.50,ZF+1.20, "cab-d2","MOBILIARIO")
box(2.50,15.20,ZF, 3.15,17.00,ZF+2.30, "arm-d2","MOBILIARIO")
# dorm3
box(4.90,15.30,ZF, 6.40,17.30,ZF+0.50, "cama-d3","MOBILIARIO")
box(4.90,15.30,ZF+0.50, 6.40,15.50,ZF+1.20, "cab-d3","MOBILIARIO")
box(3.35,15.40,ZF, 3.95,17.20,ZF+2.30, "arm-d3","MOBILIARIO")
# trastero
box(6.55,13.20,ZF, 7.00,17.40,ZF+2.00, "estant-trast","MOBILIARIO")

# ================================================================ FASE 10: MOBILIARIO P.A. (z=ZPA)
box(2.00,2.40,ZPA, 5.00,3.10,ZPA+0.70, "sofa-pa","MOBILIARIO")
box(2.40,4.60,ZPA, 4.00,6.20,ZPA+0.75, "mesa-com-pa","MOBILIARIO")
box(2.60,6.98,ZPA+0.90, 4.20,7.32,ZPA+1.80, "tv-pa","MOBILIARIO")
box(1.60,0.30,ZPA, 2.20,0.90,ZPA+0.45, "butaca-pa","MOBILIARIO")
box(6.55,4.55,ZPA, 10.25,4.90,ZPA+0.92, "encim-s-pa","MOBILIARIO")
box(10.05,0.60,ZPA, 10.35,4.50,ZPA+0.92, "encim-e-pa","MOBILIARIO")
box(7.60,2.20,ZPA, 9.20,2.70,ZPA+0.92, "isla-pa","MOBILIARIO")
box(7.55,2.15,ZPA+0.92, 9.25,2.75,ZPA+0.96, "isla-top-pa","MOBILIARIO")
box(9.55,0.40,ZPA, 10.00,1.10,ZPA+1.80, "frigo-pa","MOBILIARIO")
box(7.00,6.30,ZPA, 8.60,6.90,ZPA+0.75, "mesa-porche-pa","MOBILIARIO")
box(1.60,7.45,ZPA, 3.60,7.80,ZPA+0.85, "lavabo-bano-pa","MOBILIARIO")
box(2.20,8.05,ZPA, 2.60,8.75,ZPA+0.40, "wc-bano-pa","MOBILIARIO")
box(5.50,7.55,ZPA, 6.40,8.65,ZPA+2.00, "ducha-bano-pa","MOBILIARIO")
box(1.60,8.85,ZPA, 3.60,9.20,ZPA+0.85, "lavabo-suite-pa","MOBILIARIO")
box(2.20,9.40,ZPA, 2.60,10.10,ZPA+0.40, "wc-suite-pa","MOBILIARIO")
box(5.50,8.95,ZPA, 6.40,10.05,ZPA+2.00, "ducha-suite-pa","MOBILIARIO")
box(4.00,11.00,ZPA, 5.80,13.00,ZPA+0.50, "cama-dppal-pa","MOBILIARIO")
box(4.00,11.00,ZPA+0.50, 5.80,11.20,ZPA+1.20, "cab-dppal-pa","MOBILIARIO")
box(1.55,10.80,ZPA, 2.05,12.60,ZPA+2.30, "arm-dppal-pa","MOBILIARIO")
box(7.00,15.60,ZPA, 8.60,17.30,ZPA+0.50, "cama-d2-pa","MOBILIARIO")
box(7.00,15.60,ZPA+0.50, 8.60,15.80,ZPA+1.20, "cab-d2-pa","MOBILIARIO")
box(10.30,13.30,ZPA, 11.20,15.00,ZPA+2.30, "arm-d2-pa","MOBILIARIO")
box(6.80,13.20,ZPA, 7.60,13.90,ZPA+0.75, "escrit-d2-pa","MOBILIARIO")
box(4.90,15.30,ZPA, 6.40,17.30,ZPA+0.50, "cama-d3-pa","MOBILIARIO")
box(4.90,15.30,ZPA+0.50, 6.40,15.50,ZPA+1.20, "cab-d3-pa","MOBILIARIO")
box(3.35,15.40,ZPA, 3.95,17.20,ZPA+2.30, "arm-d3-pa","MOBILIARIO")
box(1.20,15.60,ZPA, 1.80,16.40,ZPA+0.40, "macetero-pat2","MOBILIARIO")

# ================================================================ FASE 11: VEGETACION
# olivo ornamental en maceton (patio central)
oct_cylinder("olivo-pot",9.2,9.5,0.45,0.0,0.70,"CONC")
box(8.95,9.25,0.70, 9.45,9.75,1.60, "olivo-trunk","WOOD")
box(8.50,8.90,1.60, 9.90,10.10,2.50, "olivo-crown1","PARCELA")
box(8.20,9.10,2.00, 9.60,9.90,2.80, "olivo-crown2","PARCELA")

# arboles (alrededores)
tree_data = [
  [-1.0,-3.2,1.4],[4.5,-3.2,1.2],[9.5,-3.2,1.5],[13.0,-3.2,1.3],
  [-1.0,20.0,1.4],[5.5,20.0,1.2],[12.0,20.0,1.4],[13.5,9.0,1.5],
  [8.0,8.5,1.6],[10.0,11.0,1.3]
]
tree_data.each_with_index{|(cx,cy,h),i|
  box(cx-0.06,cy-0.06,0.0, cx+0.06,cy+0.06,h*0.55, "trunk#{i}","WOOD")
  box(cx-h*0.35,cy-h*0.35,h*0.55, cx+h*0.35,cy+h*0.35,h*0.85, "crown1-#{i}","PARCELA")
  box(cx-h*0.25,cy-h*0.25,h*0.70, cx+h*0.25,cy+h*0.25,h*1.0, "crown2-#{i}","PARCELA")}

# plantas en maceta
plant_data = [
  [7.0,5.4,1.0],[10.9,5.4,1.0],[3.0,0.1,0.8],[8.0,0.1,0.8],
  [0.6,15.0,1.0],[2.6,15.0,1.0],[1.7,4.6,1.1],[6.1,11.5,0.8],
  [2.6,16.5,0.9],[10.9,16.8,0.8],[1.7,11.6,1.1]
]
plant_data.each_with_index{|(cx,cy,h),i|
  box(cx-0.12,cy-0.12,0.0, cx+0.12,cy+0.12,h*0.30, "maceta#{i}","CONC")
  box(cx-h*0.25,cy-h*0.25,h*0.30, cx+h*0.25,cy+h*0.25,h*0.70, "hojas#{i}","PARCELA")}

# ================================================================ FASE 12: COCHE
box(8.30,14.60,ZF, 10.10,17.40,ZF+0.30, "coche-chasis","MOBILIARIO")
box(8.60,14.90,ZF+0.30, 9.80,17.10,ZF+1.10, "coche-cuerpo","MOBILIARIO")
box(8.80,15.20,ZF+1.10, 9.60,16.50,ZF+1.50, "coche-techo","VENTANAS")
box(8.20,14.50,ZF-0.05, 8.50,14.80,ZF+0.10, "rueda-dl","MOBILIARIO")
box(9.90,14.50,ZF-0.05, 10.20,14.80,ZF+0.10, "rueda-dr","MOBILIARIO")
box(8.20,17.20,ZF-0.05, 8.50,17.50,ZF+0.10, "rueda-il","MOBILIARIO")
box(9.90,17.20,ZF-0.05, 10.20,17.50,ZF+0.10, "rueda-ir","MOBILIARIO")

# ================================================================ FASE 13: ARQUITECTURA EXTERIOR CONTEMPORÁNEA
SOCO_Z = 1.10

# --- zócalo corrido oscuro (sobresale 4 cm)
box(-0.02,-0.17,ZF, 11.42,-0.13,SOCO_Z, "zocalo-sur","MUROS")
box(-0.02,17.73,ZF, 11.42,17.77,SOCO_Z, "zocalo-norte","MUROS")
box(11.57,-0.02,ZF, 11.61,17.62,SOCO_Z, "zocalo-este","MUROS")
box(-0.01,-0.02,ZF, 0.03,17.62,SOCO_Z, "zocalo-oeste","MUROS")

# --- comisa de forjado (marca la P.A., sobresale 10 cm)
box(-0.10,-0.26,ZHB, 11.50,-0.14,ZHB+0.16, "comisa-sur","MUROS")
box(-0.10,17.74,ZHB, 11.50,17.86,ZHB+0.16, "comisa-norte","MUROS")
box(11.54,-0.02,ZHB, 11.66,17.62,ZHB+0.16, "comisa-este","MUROS")

# --- sombra bajo comisa (efecto volumen flotante)
box(-0.08,-0.27,2.88, 11.48,-0.13,2.90, "sombra-comisa","METAL")

# --- marquesinas sobre los dos portales
box(0.28,-1.00,2.72, 1.32,-0.14,2.80, "marquesina-A","METAL")
box(10.38,-1.00,2.72, 11.42,-0.14,2.80, "marquesina-B","METAL")

# --- portals monumentales (madera oscura, sobresalen 0.40m)
# Portal A
box(0.10,-0.55,0.22, 0.30,-0.15,2.80, "portal-A-izq","WOOD")
box(1.30,-0.55,0.22, 1.50,-0.15,2.80, "portal-A-der","WOOD")
box(0.10,-0.55,2.70, 1.50,-0.15,2.80, "portal-A-dint","WOOD")
# Portal B
box(10.20,-0.55,0.22, 10.40,-0.15,2.80, "portal-B-izq","WOOD")
box(11.40,-0.55,0.22, 11.60,-0.15,2.80, "portal-B-der","WOOD")
box(10.20,-0.55,2.70, 11.60,-0.15,2.80, "portal-B-dint","WOOD")

# --- apliques de iluminación junto a los portales
box(0.06,-0.16,2.30, 0.16,-0.08,2.50, "aplique-A","METAL")
box(11.24,-0.16,2.30, 11.34,-0.08,2.50, "aplique-B","METAL")

# --- celosía brise-soleil de madera frente al salón (P.A.)
k=0; x=1.42
while x < 6.28
  box(x-0.02,-0.24,3.00, x+0.02,-0.12,5.70, "lama-sal#{k}","WOOD")
  k+=1; x+=0.12
end

# --- panel de cristal del balcón
box(6.40,7.55,BZ0+0.06, 11.40,7.65,BZ1, "balc-cristal","VENTANAS")

# --- madera termotratada en volumen dorm2 (sobre cochera)
box(6.40,13.00,ZPA, 6.44,17.60,ZHA, "madera-d2-o","WOOD")
box(11.36,13.00,ZPA, 11.40,17.60,ZHA, "madera-d2-e","WOOD")
box(6.40,17.56,ZPA, 11.40,17.60,ZHA, "madera-d2-n","WOOD")

# --- jardineras empotradas en fachada sur (entre ventanas del salón)
box(4.40,-0.26,2.90, 4.80,-0.14,3.20, "jard-fach-1","CONC")
box(4.45,-0.24,3.20, 4.75,-0.16,3.45, "jard-hojas-1","PARCELA")
box(6.00,-0.26,2.90, 6.90,-0.14,3.20, "jard-fach-2","CONC")
box(6.10,-0.24,3.20, 6.80,-0.16,3.45, "jard-hojas-2","PARCELA")
box(9.90,-0.26,2.90, 10.40,-0.14,3.20, "jard-fach-3","CONC")
box(9.95,-0.24,3.20, 10.35,-0.16,3.45, "jard-hojas-3","PARCELA")

# --- iluminación arquitectónica lineal (LED)
box(-0.08,-0.27,2.88, 11.48,-0.13,2.90, "led-comisa-sur","LED")
box(-0.08,17.73,2.88, 11.48,17.87,2.90, "led-comisa-n","LED")
box(0.30,-0.98,2.70, 1.30,-0.16,2.72, "led-marq-A","LED")
box(10.40,-0.98,2.70, 11.40,-0.16,2.72, "led-marq-B","LED")

# --- patio como outdoor room: banco corrido + fuente
box(11.10,7.60,ZPA, 11.40,13.00,ZPA+0.45, "banco-patio","MUROS")
box(11.10,7.60,ZPA+0.45, 11.40,13.00,ZPA+0.50, "banco-patio-top","MOBILIARIO")
box(8.00,8.00,ZPA, 8.50,8.50,ZPA+0.25, "fuente-patio","CONC")

"OK build v2 completo"