#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
echo $USER;hostname;date
./sigmaModel -cl -s 1e5 -t "$1" -alg lexic,metropolis
