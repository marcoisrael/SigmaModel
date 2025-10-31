#!/usr/bin/python3
import re
import os

HOME = "/home/israel"
SRC = f"{HOME}/citations/citations.bib"
DST = "citations.bib"

# --- Copiar archivo si existe ---
if os.path.isfile(SRC):
    os.system(f"cp {SRC} {DST}")
    print("archivo actualizado")

# --- Leer contenido ---
with open(DST, "r", encoding="utf-8") as f:
    file = f.read()

# --- LIMPIEZA DE ESCAPES LaTeX ---
# Convierte "\$" -> "$" y "\_" -> "_"
file = re.sub(r"\\\$", "$", file)
file = re.sub(r"\\_", "_", file)
file = re.sub(r"\{\\textasciicircum\}", "^", file)

# --- Procesamiento habitual ---
cite_list = file.split("@")
outlines = []

for cite in cite_list[1:]:
    if re.search("article", cite):
        regexp = "@article|title =|volume =|doi =|journal =|author =|year ="
        if re.search("pages", cite):
            regexp = f"{regexp}|pages ="
        else:
            regexp = f"{regexp}|number"
        for line in f"@{cite}".splitlines():
            if re.search(regexp, line):
                outlines.append(f"{line}\n")

    elif re.search("book", cite):
        cite = cite.replace("book", "article")
        cite = cite.replace("publisher", "journal")
        regexp = "@article|\ttitle =|doi =|journal =|author =|year =|pages ="
        for line in f"@{cite}".splitlines():
            if re.search(regexp, line):
                outlines.append(f"{line}\n")

    outlines.append("}\n\n")

# --- Guardar salida ---
with open("bibliography.bib", "w", encoding="utf-8") as out:
    out.writelines(outlines)

print("archivo generado")
