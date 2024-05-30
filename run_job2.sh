#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --partition=QuantPhysMC
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=12:00:00
echo $USER;hostname;date
./sigmaModel --therm=4,0,30 -s 1e6 -alg lexic,metropolis
