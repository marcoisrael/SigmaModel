#!/bin/bash
#SBATCH --job-name=MarkovChain
#SBATCH --output=logs/MarkovChain_%j.out
#SBATCH --nodes=1
#SBATCH --partition=QuantPhysMC
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=6:00:00
#SBATCH --array=0,1,2,3,4,5,6,7,8
values="0.75 0.8 0.9 1.0 1.2 1.4 1.6 1.8 2.0"
spvalues="4 3 1 1 1 1 1 1 1"
sarr=($spvalues)
arr=($values)
echo $USER;hostname;date
echo "./sigmaModel -r -s 1e5 -alg "$1" -sp ${sarr[${SLURM_ARRAY_TASK_ID}]} -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$2""
./sigmaModel -r -s 1e5 -alg "$1" -sp ${sarr[${SLURM_ARRAY_TASK_ID}]} -t ${arr[${SLURM_ARRAY_TASK_ID}]} -l "$2" 
