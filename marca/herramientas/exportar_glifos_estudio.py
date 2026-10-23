"""Exporta "Senda", "SENDA", "CONSULTORA" y "ESTUDIO" convertidos a vectores (con kerning) en las cuatro
tipografías evaluadas, para el estudio interactivo de marca.

Uso: python3 exportar_glifos_estudio.py <carpeta_fuentes> <salida.json>
Unidades: cuerpo 1000, eje y hacia abajo, línea base en 0.
"""
import json, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from exportar_glifos import glyphs
from fontTools.ttLib import TTFont

FONTS = {
    "redhat":     {"display": "RHD-800.ttf", "desc": {"300": "RHD-300.ttf", "400": "RHD-400.ttf", "500": "RHD-500.ttf"}},
    "spectral":   {"display": "Spectral_wght_800.ttf", "desc": {"300": "Spectral_wght_300.ttf", "400": "Spectral_wght_400.ttf", "500": "Spectral_wght_500.ttf"}},
    "bodoni":     {"display": "Bodoni_Moda_opsz_wght_96_800.ttf", "desc": {"400": "Bodoni_Moda_opsz_wght_28_400.ttf", "500": "Bodoni_Moda_opsz_wght_28_500.ttf"}},
    "instrument": {"display": "Instrument_Sans_wdth_wght_75_700.ttf", "desc": {"400": "Instrument_Sans_wdth_wght_100_400.ttf", "500": "Instrument_Sans_wdth_wght_100_500.ttf"}},
}

def cap(path):
    f = TTFont(path); return round(f["OS/2"].sCapHeight * 1000 / f["head"].unitsPerEm, 1)

fd, dst = sys.argv[1], sys.argv[2]
out = {}
for key, spec in FONTS.items():
    d = f"{fd}/{spec['display']}"
    out[key] = {
        "title": glyphs(d, "Senda"), "caps": glyphs(d, "SENDA"), "cap": cap(d),
        "desc": {w: glyphs(f"{fd}/{p}", "CONSULTORA") for w, p in spec["desc"].items()},
        "descCap": {w: cap(f"{fd}/{p}") for w, p in spec["desc"].items()},
        "descEstudio": {w: glyphs(f"{fd}/{p}", "ESTUDIO") for w, p in spec["desc"].items()},
    }
json.dump(out, open(dst, "w"), separators=(",", ":"))
print("ok", {k: v["cap"] for k, v in out.items()})
