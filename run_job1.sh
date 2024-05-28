#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
echo $USER;hostname;date
./sigmaModel -r -s 1e5 -alg lexic,metropolis -t "$1"
