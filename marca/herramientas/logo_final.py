"""Genera los SVG finales del logo de Senda (S Contrapeso + Red Hat Display, paleta Fiordo).

Parámetros definidos en el estudio de marca (ver PARAMS). Todo en vectores: no depende de
que la tipografía esté instalada.

Uso: python3 logo_final.py <glifos-estudio.json> <carpeta_salida>
"""
import json, sys, os

PARAMS = dict(font="redhat", cas="title", track=-25, scale=1.4, sep=0.85, align="center",
              desc=200, descW="500", lead=115)

COLORES = {
    "pizarra": "#16232B", "naranja": "#FF5B04", "verde": "#075056", "niebla": "#E4EEF0",
}
# nombre de variante: (color de la S, color del texto, fondo sugerido para la vista previa)
VARIANTES = {
    "positivo":      ("#FF5B04", "#16232B", "#E4EEF0"),   # sobre fondos claros
    "negativo":      ("#FF5B04", "#E4EEF0", "#16232B"),   # sobre pizarra (principal de la marca)
    "sobre-verde":   ("#E4EEF0", "#E4EEF0", "#075056"),
    "sobre-naranja": ("#16232B", "#16232B", "#FF5B04"),
    "mono-pizarra":  ("#16232B", "#16232B", "#FFFFFF"),
    "mono-blanco":   ("#FFFFFF", "#FFFFFF", "#16232B"),
    "mono-negro":    ("#000000", "#000000", "#FFFFFF"),
}

def f(v): return f"{v:.2f}".rstrip("0").rstrip(".")

def contrapeso(H, x, y):
    """S Contrapeso en su caja exacta (grilla 100: x16..84, y8..92), escalada a alto H en (x, y)."""
    s = H / 84.0
    P = lambda a, b: (x + (a - 16) * s, y + (b - 8) * s)
    r = 21 * s
    def piece(rot):
        q = (lambda a, b: P(100 - a, 100 - b)) if rot else P
        a1, a2, a3, a4 = q(48, 8), q(84, 8), q(84, 29), q(48, 29)
        b1, b2 = q(48, 8), q(48, 50)
        rect = f"M{f(a1[0])} {f(a1[1])} L{f(a2[0])} {f(a2[1])} L{f(a3[0])} {f(a3[1])} L{f(a4[0])} {f(a4[1])} Z"
        half = f"M{f(b1[0])} {f(b1[1])} A{f(r)} {f(r)} 0 0 0 {f(b2[0])} {f(b2[1])} Z"
        return rect + " " + half
    return piece(False) + " " + piece(True), 68 * s

def place(glyphs, dx, dy, k=1.0, track=0.0, x0=0.0):
    out = []
    for i, g in enumerate(glyphs):
        tx = dx + (g["x"] * k - x0) + i * track
        tr = f"translate({f(tx)} {f(dy)})" + (f" scale({k})" if k != 1 else "")
        out.append(f'<path transform="{tr}" d="{g["d"]}"/>')
    return "".join(out)

MEDIDAS = {}

def build(G, kind):
    p = PARAMS; F = G[p["font"]]; S = F[p["cas"]]; C = F["desc"][p["descW"]]; dcap = F["descCap"][p["descW"]]
    t = p["track"]; n = len(S)
    inkL = S[0]["x"] + S[0]["b"][0]
    W = S[-1]["x"] + (n - 1) * t + S[-1]["b"][2] - inkL
    sTop = S[0]["b"][1]; top = min(g["b"][1] for g in S); bottom = max(g["b"][3] for g in S)
    k = p["desc"] / 1000; m = len(C)
    c0 = (C[0]["x"] + C[0]["b"][0]) * k
    cw0 = (C[-1]["x"] + C[-1]["b"][2]) * k - c0
    tc = (W - cw0) / (m - 1)
    capD = dcap * k
    descBase = (p["lead"] / 100) * capD + capD
    descBottom = descBase + max(g["b"][3] for g in C) * k

    if kind in ("principal", "corta"):
        withD = kind == "principal"
        base = descBase if withD else 0
        blockH = base - sTop
        H = blockH * p["scale"]
        mTop = sTop + blockH / 2 - H / 2
        mark, mw = contrapeso(H, 0, mTop)
        mx = mw + p["sep"] * blockH * 0.25
        word = place(S, mx - inkL, 0, 1, t)
        desc = place(C, mx, descBase, k, tc, c0) if withD else ""
        y0 = min(mTop, top); y1 = max(mTop + H, descBottom if withD else bottom)
        vb = (0, y0, mx + W, y1 - y0)
        if withD:
            MEDIDAS.update(H=H, blockH=blockH, markTop=mTop, markW=mw, textX=mx, textW=W, sTop=sTop,
                           descTop=descBase - capD, descBase=descBase, bar=H * 21 / 84, gap=mx - mw)
    elif kind == "vertical":
        capS = -sTop
        H = capS * 1.55
        gap = capS * 0.5
        mark, mw = contrapeso(H, (W - H * 68 / 84) / 2, 0)
        base = H + gap + capS
        word = place(S, -inkL, base, 1, t)
        desc = place(C, 0, base + descBase, k, tc, c0)
        vb = (0, 0, W, base + descBottom)
    else:  # monograma
        mark, mw = contrapeso(840, 0, 0)
        word = desc = ""
        vb = (0, 0, mw, 840)
    return mark, word, desc, vb

def svg(parts, mark_c, ink_c, title):
    mark, word, desc, vb = parts
    v = " ".join(f(x) for x in vb)
    body = f'<path fill="{mark_c}" d="{mark}"/>'
    if word: body += f'<g fill="{ink_c}">{word}{desc}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{v}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

def main(src, outdir):
    G = json.load(open(src)); os.makedirs(outdir, exist_ok=True)
    index = {}
    for kind in ("principal", "corta", "vertical", "monograma"):
        parts = build(G, kind)
        for var, (mc, ic, bg) in VARIANTES.items():
            name = f"senda-{kind}-{var}.svg"
            open(f"{outdir}/{name}", "w").write(svg(parts, mc, ic, "Senda Consultora"))
            index[name] = {"version": kind, "variante": var, "fondo": bg, "viewBox": [round(x, 2) for x in parts[3]]}
    json.dump({"params": PARAMS, "colores": COLORES, "medidas": {k: round(v, 2) for k, v in MEDIDAS.items()}, "archivos": index}, open(f"{outdir}/indice.json", "w"), indent=1, ensure_ascii=False)
    print(len(index), "archivos")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
