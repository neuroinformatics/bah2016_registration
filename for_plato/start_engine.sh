#!/bin/bash

#$ -S /bin/bash
#$ -V
#$ -j y
#$ -N ipengine
#$ -cwd
#$ -pe impi 152
#$ -q all.q

export I_MPI_DEVICE=ssm
COMMAND=ipengine

mpirun -genv I_MPI_FABRICS shm:ofa -np $NSLOTS $COMMAND
