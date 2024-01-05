#!/usr/bin/python3
from loaddata import *
startTemp = 4
for endTemp in [0]:
    path = f"output/cooling/L64/{startTemp}-{endTemp}"
    dest = f"output/plot/L64/{startTemp}-{endTemp}"
    dt = loadData("Multi", "Cluster", startTemp, endTemp, path, dest)
    dt.plot([3,6,9,12,15])
    for method in ["Random", "Lexic"]:
        for alg in  ["Glauber", "Metropolis"]:
            dt = loadData(method, alg, startTemp, endTemp, path, dest)
            dt.plot([3,6,9,12,15])
