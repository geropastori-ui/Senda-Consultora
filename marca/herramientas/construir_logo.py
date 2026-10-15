"""Construye el logo de Senda (Bisel + Red Hat Display) con letras convertidas a vectores.

Reglas de construcción (unidades de la fuente, "Senda" a 1000 de cuerpo):
- "Senda": Red Hat Display ExtraBold (800). Altura de mayúscula 700.
- "CONSULTORA": Red Hat Display Regular (400), cuerpo DESC_SIZE, interletrado calculado
  para que el ancho de tinta sea exactamente el de "Senda".
- Separación entre línea base de "Senda" y tope de "CONSULTORA": GAP_LINES.
- La S (Bisel) mide de alto desde el tope de la "S" hasta la línea base de "CONSULTORA".
- Espacio entre la S y el texto = grosor de la barra del Bisel (21/84 de su alto).

Uso: python3 construir_logo.py <carpeta_fuentes> <archivo_salida.json>
"""
import json, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

DESC_SIZE = 245
GAP_LINES = 120

def load(path):
    blob = hb.Blob.from_file_path(path)
    return TTFont(path), hb.Font(hb.Face(blob))

def shape(fonts, text, size, tracking=0.0):
    tt, hbf = fonts
    upm = tt['head'].unitsPerEm
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbf, buf, {"kern": True, "liga": False})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    scale = size / upm
    x = 0.0; glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyphs.append((order[info.codepoint], x + pos.x_offset * scale))
        x += pos.x_advance * scale + tracking
    return glyphs, gs, scale

def render(fonts, text, size, tracking, dx, base_y):
    """Devuelve (path_d, bbox) con y hacia abajo; base_y es la línea base en coordenadas SVG."""
    glyphs, gs, scale = shape(fonts, text, size, tracking)
    d = []; bx = [1e9, 1e9, -1e9, -1e9]
    for name, x in glyphs:
        g = gs[name]
        bp = BoundsPen(gs); g.draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            bx = [min(bx[0], dx + x + x0*scale), min(bx[1], base_y - y1*scale),
                  max(bx[2], dx + x + x1*scale), max(bx[3], base_y - y0*scale)]
        sp = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip('0').rstrip('.'))
        g.draw(TransformPen(sp, (scale, 0, 0, -scale, dx + x, base_y)))
        d.append(sp.getCommands())
    return " ".join(d), bx

def ink_width(fonts, text, size, tracking):
    _, bx = render(fonts, text, size, tracking, 0, 0)
    return bx[2] - bx[0], bx[0]

def bisel(h, x, y):
    """Bisel en su caja exacta (x16..84, y8..92 en la grilla de 100), escalado a alto h."""
    s = h / 84.0
    top = [(84,8),(40,8),(27,21),(27,37),(40,50),(48,50),(48,29),(84,29)]
    bot = [(100-a, 100-b) for a, b in top]
    pt = lambda p: f"{x + (p[0]-16)*s:.2f},{y + (p[1]-8)*s:.2f}"
    return " ".join("M" + " L".join(pt(p) for p in poly) + " Z" for poly in (top, bot)), 68*s

def main(fontdir, out):
    bold = load(f"{fontdir}/RHD-800.ttf"); reg = load(f"{fontdir}/RHD-400.ttf")
    W, x0 = ink_width(bold, "Senda", 1000, 0)
    # interletrado de CONSULTORA para igualar el ancho de tinta de "Senda"
    lo, hi = -50.0, 400.0
    for _ in range(60):
        mid = (lo + hi) / 2
        w, _ = ink_width(reg, "CONSULTORA", DESC_SIZE, mid)
        lo, hi = (mid, hi) if w < W else (lo, mid)
    track = (lo + hi) / 2

    # --- horizontal completo ---
    _, sb = render(bold, "Senda", 1000, 0, 0, 0)
    s_top = sb[1]                                   # tope de tinta de la "S" (la d sube un poco más)
    _, sbS = render(bold, "S", 1000, 0, 0, 0); s_top = sbS[1]
    cap_desc = 700 * DESC_SIZE / 1000
    desc_base = GAP_LINES + cap_desc               # línea base de CONSULTORA, con la de Senda en 0
    H = desc_base - s_top
    mark, mw = bisel(H, 0, 0)
    gap = H * 21 / 84
    tx = mw + gap - x0
    word, wb = render(bold, "Senda", 1000, 0, tx, -s_top)
    _, cx0 = ink_width(reg, "CONSULTORA", DESC_SIZE, track)
    desc, db = render(reg, "CONSULTORA", DESC_SIZE, track, tx + x0 - cx0, -s_top + desc_base)
    top_all = min(0, wb[1]); right = max(wb[2], db[2])
    full = {"mark": mark, "word": word, "desc": desc,
            "viewBox": [0, round(top_all, 2), round(right, 2), round(H - top_all, 2)]}

    # --- horizontal corto (sin descriptor): S = 1,3 × altura de la S, centrada en ella ---
    capS = -s_top
    H2 = capS * 1.3
    mark2, mw2 = bisel(H2, 0, 0)
    gap2 = H2 * 21 / 84
    word2, wb2 = render(bold, "Senda", 1000, 0, mw2 + gap2 - x0, H2/2 + capS/2)
    short = {"mark": mark2, "word": word2,
             "viewBox": [0, round(min(0, wb2[1]), 2), round(wb2[2], 2), round(H2 - min(0, wb2[1]), 2)]}

    # --- vertical: S arriba, texto centrado ---
    H3 = capS * 1.45
    gap3 = H3 * 0.30
    Wtxt = W
    mark3, mw3 = bisel(H3, (Wtxt - 68*H3/84)/2, 0)
    base3 = H3 + gap3 + capS
    word3, wb3 = render(bold, "Senda", 1000, 0, -x0, base3)
    desc3, db3 = render(reg, "CONSULTORA", DESC_SIZE, track, -cx0, base3 + desc_base)
    vert = {"mark": mark3, "word": word3, "desc": desc3,
            "viewBox": [0, 0, round(Wtxt, 2), round(db3[3], 2)]}

    json.dump({"full": full, "short": short, "vertical": vert,
               "rules": {"descSize": DESC_SIZE, "tracking": round(track, 2), "gapLines": GAP_LINES,
                         "markHeight": round(H, 2), "markGap": round(gap, 2), "inkWidth": round(W, 2)}},
              open(out, "w"))
    print("tracking CONSULTORA:", round(track, 1), "| alto S:", round(H, 1), "| ancho Senda:", round(W, 1))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
