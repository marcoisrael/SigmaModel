#!/bin/bash
#SBATCH --job-name=SigmaModelLM
#SBATCH --output=logs/SigmaModelLM/SigmaModelLM_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=1:00:00
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e4"
alg="lexic,metropolis"
name="v64x64/4p0-1p5"
./sigmaModel -cool "4,1.5,6" -s "$N" -alg "$alg" -n "$name"
