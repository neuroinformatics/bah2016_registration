# bah2016_registration
Brain Atlas Hackathon Registration Team

## directories
- input dirs


## usage

### Parallelized registration with itk and ipyparallel
1. start ipyparallel controller
```
$ ipcontroller ip=*
```
1. start ipython engine by SGE (MPI)
```
$ qsub start_engine.sh
```

- start_engine.sh is like:
```bash
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
```

1. start registration job
```
$ cd registration
$ python ParaRegistration.py
```


### Matching brain regiona

### Draw color chart
