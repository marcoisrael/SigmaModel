#!/bin/bash
#SBATCH --job-name=SigmaModelMC
#SBATCH --output=logs/SigmaModelMC/SigmaModelMC_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=1:00:00
#SBATCH --array=3-15:3
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e4"
alg="multi,cluster"
name="v64x64/4p0-1p0"
./sigmaModel -cool "4,1,${SLURM_ARRAY_TASK_ID}" -s "$N" -alg "$alg" -n "$name"
