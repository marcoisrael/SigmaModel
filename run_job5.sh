#!/bin/bash
#SBATCH --job-name=SigmaModelSC
#SBATCH --output=logs/SigmaModelSC_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=4:00:00
#SBATCH --array=5-20:5
module load lamod/gcc/12.2
hostname;date
N="1e4"
alg="single,cluster"
name="v64x64t4-0"
./sigmaModel -cool "4,0,${SLURM_ARRAY_TASK_ID}"  -s "$N" -alg "$alg" -n "$name"
