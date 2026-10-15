#!/bin/bash -l
#SBATCH -J rennwagen
#SBATCH -p compute
#SBATCH -N 1
#SBATCH --ntasks-per-node=12
#SBATCH -t 02:00:00
#SBATCH -o slurm-%j.out

module load OpenFOAM/v2012-foss-2020a
source $FOAM_BASH
export SLURM_CPU_BIND=none

cd $SLURM_SUBMIT_DIR
mpirun -np 12 rhoCentralFoam -parallel > log.rhoCentralFoam 2>&1
