#!/bin/bash
#SBATCH --job-name=SigmaModelLG
#SBATCH --output=logs/SigmaModelLG/SigmaModelLG_%j.out
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=100mb
#SBATCH --time=1:00:00
#SBATCH --array=3-15:3
module load lamod/gcc/12.2
echo $USER;hostname;date
N="1e4"
alg="lexic,glauber"
endTemp="0"
name="L64/4-${endTemp}"
./sigmaModel -cool "4,${endTemp},${SLURM_ARRAY_TASK_ID}" -s "$N" -alg "$alg" -n "$name"
