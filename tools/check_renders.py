from PIL import Image
import glob, os
for p in sorted(glob.glob('entrega/renders/sketchup/*.png')):
    im = Image.open(p).convert('RGB')
    px = list(im.getdata())
    n = len(px)
    nw = sum(1 for r,g,b in px if (r,g,b)!=(255,255,255))
    colors = {}
    for c in px:
        colors[c] = colors.get(c, 0) + 1
    top = sorted(colors.items(), key=lambda x: -x[1])[:3]
    print(f"{os.path.basename(p):25s} content={nw*100//n:2d}% {os.path.getsize(p)//1024:3d}KB  top: {', '.join(f'rgb{c}:{v*100//n}%%' for c,v in top)}")
