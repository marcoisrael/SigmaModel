#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=2:00:00
#SBATCH --array=1-20:1
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e4"
name="earlyUniverse/4-0.1"
./sigmaModel -cool "0.0625,100,${SLURM_ARRAY_TASK_ID}" -s "$N" -alg "$1" -n "$name"
