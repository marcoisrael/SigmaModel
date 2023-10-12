#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
for i in [20, 40, 80]:
    data = np.loadtxt(f"output/susceptibility/{i}.tsv", skiprows=1)
    step, temp,sucept, suceptError = data.transpose()
    plt.errorbar(step, sucept, yerr=suceptError, marker='.', ls='', label=r'$\tau_Q=$'+str(i))
    plt.xlabel('#sweeps')
    plt.ylabel('susceptibility')
plt.savefig('output/plot/metropolis.png')