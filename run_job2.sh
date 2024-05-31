#!/bin/bash
#SBATCH --job-name=thermalized
#SBATCH --output=logs/Thermalized_%j.out
#SBATCH --nodes=1
#SBATCH --partition=QuantPhysMC
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=12:00:00
echo $USER;hostname;date
echo '/sigmaModel --therm=4,0,30 -s 1e5 -alg lexic,metropolis'
./sigmaModel --therm=4,0,30 -s 1e5 -alg lexic,metropolis
