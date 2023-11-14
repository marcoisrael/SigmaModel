#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=2:00:00
#module load lamod/gcc/12.2
hostname;date
N="1e5"
alg=$1
./sigmaModel -cool 4,0,5 -s "$N" -alg "$alg"
./sigmaModel -cool 4,0,10 -s "$N" -alg "$alg"
./sigmaModel -cool 4,0,15 -s "$N" -alg "$alg"
./sigmaModel -cool 4,0,20 -s "$N" -alg "$alg"




