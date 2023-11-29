#!/bin/bash
#SBATCH --job-name=SigmaModelRM
#SBATCH --output=logs/SigmaModelRM_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=1:00:00
#SBATCH --array=3-15:3
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e4"
alg="random,metropolis"
name="v64x64/4p0-0p0"
./sigmaModel -cool "4,0,${SLURM_ARRAY_TASK_ID}"  -s "$N" -alg "$alg" -n "$name"
