#!/usr/bin/python
import os
plot_files = [
            "cone",
            "distribution",
            "sphere",
            "discont",
            "lattice",
            "thermalization",
            "toro",
            ]

for pfile in plot_files:
    os.system(f"python mkplots/{pfile}.py")
