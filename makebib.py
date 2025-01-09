#!/usr/bin/python3
import re

file = open("citations.bib").read()
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
    if re.search("book", cite):
        cite = cite.replace("book", "article")
        cite = cite.replace("publisher", "journal")
        regexp = "@article|\ttitle =|doi =|journal =|author =|year =|pages ="
        for line in f"@{cite}".splitlines():
            if re.search("@book|@incollection", line):
                outlines.append(f"{line}\n".replace)
            if re.search(regexp, line):
                outlines.append(f"{line}\n")
    outlines.append("}\n\n")


outfile = open("bibliography.bib", "w")
outfile.writelines(outlines)
