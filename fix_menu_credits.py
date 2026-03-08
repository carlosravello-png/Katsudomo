import os
import re

base_dir = r"c:\Users\RAVELLO CAMACHO\Documents\GitHub\Katsudomo"

html_files = [
    os.path.join(base_dir, "menu", "carta.html"),
    os.path.join(base_dir, "ja", "menu", "carta.html")
]

credit_es = '<p class="author-credits">Diseño y autoría por Carlos Ravello Joo &nbsp;&bull;&nbsp; Modelo de Coherencia Dinámica &nbsp;&bull;&nbsp; Todos los derechos reservados</p>'

for fp in html_files:
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        if "author-credits" not in content:
            # specifically search for © 2026
            content = re.sub(r'(<p>[^<]*©[^<]*</p>)', r'\1\n            ' + credit_es, content)
            
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)

print("Créditos inyectados en los menús que faltaban.")
