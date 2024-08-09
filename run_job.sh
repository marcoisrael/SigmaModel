#!/bin/bash
#SBATCH --job-name=CorrelationLength
#SBATCH --output=logs/CorrelationLength_%j.out
#SBATCH --nodes=1
#SBATCH --partition=QuantPhysMC
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
#SBATCH --array=0
values="0.75 0.8 0.85 0.9 0.95 1.0 2.0 3.0 4.0"
arr=($values)
echo $USER;hostname;date
echo './sigmaModel -cl -s 1e5 -alg lexic,metropolis -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$1"'
./sigmaModel -cl -s 1e5 -alg lexic,metropolis -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$1"
