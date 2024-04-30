#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
echo $USER;hostname;date
N="1e4"
./sigmaModel -r -t "$1" -s "$N" -alg "$2" -d "$3" -sp "$4"
