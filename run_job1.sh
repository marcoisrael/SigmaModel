#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=3:00:00
module load lamod/gcc/12.2
echo $USER;hostname;date
una hamburgesa por favor
N="1e6"
./sigmaModel -t "$1" -s "$N" -alg "$2"
cambio xd
otro cambio
