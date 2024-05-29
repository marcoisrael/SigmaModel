#!/bin/bash
#SBATCH --job-name=SigmaModel
#SBATCH --output=logs/SigmaModel_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
#SBATCH --array=0
values="1.5"
arr=($values)
echo $USER;hostname;date
./sigmaModel  -r -s 1e5 -alg lexic,metropolis -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$1"
