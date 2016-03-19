#!/usr/bin/env python
#coding: UTF-8

from ipyparallel import Client

def singlejob(arg):
    import subprocess
    import os

    filename = arg
    filename_base, filename_ext = os.path.splitext(filename)
    homedir = '/data/registration/Processed/'
    sbfile_base  = homedir + 'SB_bin/Reslice_WHS_0.6.1_Labels_fixed_bin%04d.tif'
    indir  = homedir + 'work3/'
    outdir = homedir + 'work4/'
    logdir = homedir + 'log4/' + filename_base + '/'
    
    RegProgram1 = '/share/apps/registration/itk/ImageRegistration/ImageRegistration9'
    command_format = RegProgram1 + ' %s %s %s'

    os.mkdir(logdir)

    for i in range(80, 121):
        sbfile = sbfile_base % i
        cmd = [RegProgram1, sbfile, indir+filename, outdir+filename_base+('_%04d.tif' % i)]
        print cmd

        ret = subprocess.check_output(cmd)

        logfilename = logdir + ('%04d.log' % i)
        with open(logfilename, mode='w') as f:
            for line in ret:
                f.write(line)


def do_parallel(filelist):
    rc = Client()

    print('# of engines : %d' % len(rc.ids))
    print('# of job : %d' % len(filelist))

    lv = rc.load_balanced_view()
    result = lv.map_async(singlejob, filelist)
    result.wait_interactive()


def do_single(filelist):
    print('# of engines : single')
    print('# of job : %d' % len(filelist))

    for arg in filelist:
        singlejob(arg)


if __name__ == '__main__':
    filelist_file = '/data/registration/filelist.txt'
    #filelist_file = '/data/registration/filelist_small.txt'


    filelist = []
    with open(filelist_file, mode='r') as f:
        filelist = f.readlines()

    filelist = [str.rstrip() for str in filelist]

    do_parallel(filelist)
    #do_single(filelist)
