"""Exporta los contornos de "Senda" (Red Hat Display 800) y "CONSULTORA" (300, 400 y 500) con su kerning,
para que la página del constructor pueda recomponer el logo con cualquier interletrado y tamaño.

Uso: python3 exportar_glifos.py <carpeta_fuentes> <salida.json>
Todo en unidades de fuente a cuerpo 1000, eje y hacia abajo, línea base en 0.
"""
import json, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

def glyphs(path, text):
    tt = TTFont(path); f = hb.Font(hb.Face(hb.Blob.from_file_path(path)))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(f, buf, {"kern": True, "liga": False})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder(); s = 1000 / tt['head'].unitsPerEm
    out = []; x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = gs[order[info.codepoint]]
        bp = BoundsPen(gs); g.draw(bp); x0, y0, x1, y1 = bp.bounds
        sp = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip('0').rstrip('.'))
        g.draw(TransformPen(sp, (s, 0, 0, -s, 0, 0)))
        out.append({"d": sp.getCommands(), "x": round((x + pos.x_offset) * s, 2),
                    "b": [round(x0*s, 1), round(-y1*s, 1), round(x1*s, 1), round(-y0*s, 1)]})
        x += pos.x_advance
    return out

if __name__ == "__main__":
  fd, dst = sys.argv[1], sys.argv[2]
  json.dump({"senda": glyphs(f"{fd}/RHD-800.ttf", "Senda"),
           "consultora": glyphs(f"{fd}/RHD-400.ttf", "CONSULTORA"),
           "consultoraPorPeso": {w: glyphs(f"{fd}/RHD-{w}.ttf", "CONSULTORA") for w in ("300", "400", "500")},
           "capHeight": 700}, open(dst, "w"))
  print("ok")
