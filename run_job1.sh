#!/bin/bash
#SBATCH --job-name=FastCooling
#SBATCH --output=logs/FastCooling_%j.out
#SBATCH --nodes=1
#SBATCH --partition=QuantPhysMC
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=24:00:00
#SBATCH --array=2,4,8,16,20
echo $USER;hostname;date
./sigmaModel -s 1e6 -alg "$1" -n "FastCooling" --cooling=4,0,${sarr[${SLURM_ARRAY_TASK_ID}]} 
