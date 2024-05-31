#!/bin/bash
#SBATCH --job-name=MarkovChain
#SBATCH --output=logs/MarkovChain_%j.out
#SBATCH --nodes=1
#SBATCH --partition=QuantPhysMC
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
#SBATCH --array=0,1
values="0.85 0.8 1.2 1.4 1.6 1.8"
arr=($values)
echo $USER;hostname;date
echo "/sigmaModel -r -s 1e5 -alg lexic,metropolis -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$1""
./sigmaModel -r -s 1e5 -alg lexic,metropolis -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$1"
