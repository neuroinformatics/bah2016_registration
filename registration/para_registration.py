# -*- coding: utf-8 -*-

import os
import sys
from ipyparallel import Client


class ParaExec:
 
    def __init__(self, addpath=None):
        self.client = Client()
        self.load_balanced_view = self.client.load_balanced_view()
        if(len(self.client.ids) == 0):
            print('# of engines : single mode')
        else:
            print('# of engines : %d' % len(self.client.ids))


    def do_parallel(self, func, arglist):
        print('# of job : %d' % len(arglist))    

        rs = self.load_balanced_view.map_async(func, arglist)
        rs.wait_interactive()
        print rs.result()


    def do_single(self, func, arglist):
        print('# of job : %d' % len(arglist))
        for arg in arglist:
            func(arg)


if __name__ == '__main__':
    def wrap_registration(filename):
        import os,sys
        sys.path.append('/data/miyamoto/git/bah2016_registration/registration')

        import BahRegistration
        reload(BahRegistration)

        reg = BahRegistration.BahRegistration(homedir='/data/registration/Test')
        metric = reg.single_registration(filename, sb_reslice_end=83)

        return metric

    def read_filelist(filelistname):
        filelist = []
        with open(filelistname, mode='r') as f:
            filelist = f.readlines()

        filelist = [str.rstrip() for str in filelist]
        return filelist

    filelistname = os.path.join('/', 'data', 'registration', 'Test', 'filelist_test.txt')
    filelist = read_filelist(filelistname)

    pec = ParaExec()
    pec.do_parallel(wrap_registration, filelist)
    #pec.do_single(wrap_registration, filelist)
