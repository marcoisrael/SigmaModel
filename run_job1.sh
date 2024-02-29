#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=3:00:00
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e6"
temp=0.5
./sigmaModel -t $temp -s "$N" -alg "$1"
