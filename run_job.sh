#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=2:00:00
module load lamod/gcc/12.2
date;hostname;pwd
N="1e5"
alg="lexic,metropolis"
./sigmaModel -cool 4,0,40 -c "$N" -alg "$alg"
