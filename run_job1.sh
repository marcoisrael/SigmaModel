#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=12:00:00
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e5"
temp=4
./sigmaModel -t $temp -s "$N" -alg "$1"
