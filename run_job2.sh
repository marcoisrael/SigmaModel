#!/bin/bash
#SBATCH --job-name=SigmaModelLG
#SBATCH --output=logs/SigmaModelLG_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=8:00:00
#SBATCH --array=4-16:4
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e4"
alg="lexic,glauber"
name="v64x64/4p0-0p5"
./sigmaModel -cool "4,0.5,${SLURM_ARRAY_TASK_ID}"  -s "$N" -alg "$alg" -n "$name"
