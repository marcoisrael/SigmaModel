#!/usr/bin/python3
from plotClass import *
startTemp = 4
endTemp = 0
tauq = np.arange(1,21)

path = f"output/cooling/jkL64/{startTemp}-{endTemp}"
dest = f"output/plot/jkL64/{startTemp}-{endTemp}"

data = loadData("Multi", "Cluster", startTemp, endTemp, path, dest,tauq)
data.fit()
data.plot()

data = loadData("Lexic", "Metropolis", startTemp, endTemp, path, dest,tauq)
data.fit()
data.plot()	

data = loadData("Random", "Metropolis", startTemp, endTemp, path, dest,tauq)
data.fit()
data.plot()

data = loadData("Lexic", "Glauber", startTemp, endTemp, path, dest,tauq)
data.fit()
data.plot()

data = loadData("Random", "Glauber", startTemp, endTemp, path, dest,tauq)
data.fit()
data.plot()
