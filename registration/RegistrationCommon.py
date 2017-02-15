# -*- coding: utf-8 -*-


def read_filelist(filelistname):
    with open(filelistname, mode='r') as f:
        filelist = f.readlines()
        
    filelist = [str.rstrip() for str in filelist]
    return filelist

