# -*- coding: utf-8 -*-

import os
from ipyparallel import Client


class ParaExec:
    """
    Parallelized execution of a function with ipyparallel
    """
    def __init__(self):
        self.client = Client()
        self.load_balanced_view = self.client.load_balanced_view()
        if len(self.client.ids) == 0:
            print('# of engines : single mode')
        else:
            print('# of engines : %d' % len(self.client.ids))

    def do_parallel(self, func, arg_list):
        print('# of job : %d' % len(arg_list))

        rs = self.load_balanced_view.map_async(func, arg_list)
        rs.wait_interactive()
        print rs.result()

    def do_single(self, func, arg_list):
        print('# of job : %d' % len(arg_list))
        for arg in arg_list:
            func(arg)


if __name__ == '__main__':
    def wrap_registration(filename):
        import os
        import sys
        registration_source_path = '/data/'
        sys.path.append(registration_source_path)

        import BahRegistration
        reload(BahRegistration)

        reg = BahRegistration.BahRegistration(homedir='/data/registration/Processed20170212')
        # metric = reg.single_registration(filename)
        metric = reg.single_registration(filename, sb_reslice_end=83)
        reg.draw_metric_graph()

        return metric

    def read_filelist(filelistname):
        filelist = []
        with open(filelistname, mode='r') as f:
            filelist = f.readlines()

        filelist = [str.rstrip() for str in filelist]
        return filelist

    filelistname = os.path.join('/', 'data', 'registration', 'Processed20170212', 'filelist.txt')
    filelist = read_filelist(filelistname)

    pec = ParaExec()
    pec.do_parallel(wrap_registration, filelist)
    # pec.do_single(wrap_registration, filelist)
