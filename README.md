# bah2016_registration
Registration method for in situ hybridization images to fMRI standard coordinated brain (e.g. Waxholm Brain Atlas).
This program was parallelized for PC clusters to increace registration speed.

Developed by Brain Atlas Hackathon Registration Team (https://www.neuroinf.jp/bah2015/?ml_lang=en)

## Dependency
- ipython
- ipyparallel
- ImageJ/Fiji
- ITK

## Files and Directories
- Parallel registration **input** dirs
    - filelist_all.txt: write down all TIF file name of *in situ* hybridization images
    - work3: Monochromed (and resized) TIF files of *in situ* hybridization images
    - SB_bin: resliced standard brain files (from Waxholm Space)

- Parallel registration **output** dirs
    - work4: results of registration for all standard brain slices
    - log4: registration log 
    - metric: metric value for each slice
    - metric_fig: graph of metric value

## usage

### Parallelized registration with itk and ipyparallel

#### start ipyparallel controller  
```
$ ipcontroller ip=*
```

#### start ipython engine by SGE (MPI)

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

#### start registration job

```
$ cd registration
$ python ParaRegistration.py
```


### Matching brain regiona

### Draw color chart
