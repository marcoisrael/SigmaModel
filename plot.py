#!/usr/bin/python3
from loaddata import *
startTemp = 4
endTemp = 1.5

path = f"output/cooling/v64x64/{tempName(startTemp,endTemp)}"
dest = f"output/plot/v64x64/{tempName(startTemp,endTemp)}"
dt = loadData("Multi", "Cluster", startTemp, endTemp, path, dest)
dt.plot([3,6,9,12,15])
for method in ["Random", "Lexic"]:
    for alg in  ["Glauber", "Metropolis"]:
        dt = loadData(method, alg, 4, 0, path, dest)
        dt.plot([3,6,9,12,15])
