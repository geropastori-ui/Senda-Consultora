"""Arma el manual de marca inyectando los SVG finales y las medidas del logo en la plantilla."""
import json, glob, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = json.load(open(f"{base}/logo/final/indice.json"))
svgs = {os.path.basename(p): open(p).read().strip() for p in sorted(glob.glob(f"{base}/logo/final/*.svg"))}
data = {"svgs": svgs, "medidas": idx["medidas"], "params": idx["params"],
        "vb": {"principal": idx["archivos"]["senda-principal-positivo.svg"]["viewBox"]}}
t = open(f"{base}/herramientas/manual.plantilla.html").read()
open(f"{base}/manual/senda-manual-de-marca.html", "w").write(t.replace("__LOGO__", json.dumps(data, ensure_ascii=False)))
print("ok", len(svgs))
