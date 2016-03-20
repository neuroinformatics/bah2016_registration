# -*- coding: utf-8 -*-

import subprocess
import os
import sys

class BahRegistration:

    def __init__(self, homedir = None):
        if homedir is None:
            homedir = os.path.join('/', 'data', 'registration', 'Processed')

        if not os.path.exists(homedir):
            sys.exit('Error : %s not found.' % homedir)

        self.homedir = homedir
        self.sbfile_base = os.path.join(homedir, 'SB_bin/Reslice_WHS_0.6.1_Labels_fixed_bin%04d.tif')
        self.registration_in = os.path.join(homedir, 'work3')
        self.registration_out = os.path.join(homedir, 'work4')
        self.registration_log = os.path.join(homedir + 'log4')
        
        if not os.path.exists(self.registration_in):
            sys.exit('Error : %s not found.' % self.registration_in)

        if not os.path.exists(self.registration_out):
            os.mkdir(self.registration_out)
        if not os.path.exists(self.registration_log):
            os.mkdir(self.registration_log)

    
    def single_registration(self, filename,
                            reg_program = '/share/apps/registration/itk/ImageRegistration/ImageRegistration9',
                            sb_reslice_start=80, sb_reslice_end=121):

        filename_base, filename_ext = os.path.splitext(filename)
        logdir = self.registration_log + filename_base + '/'

        if not os.path.exists(logdir):
            os.mkdir(logdir)
        for i in range(sb_reslice_start, sb_reslice_end):
            sbfile = self.sbfile_base % i
            inputfile = os.path.join(self.registration_in, filename)
            outputfile = os.path.join(self.registration_out, filename_base+('_%04d.tif' % i))
            
            cmd = [reg_program, sbfile, inputfile, outputfile]
            print cmd

            ret = subprocess.check_output(cmd)

            logfilename = logdir + ('%04d.log' % i)
            with open(logfilename, mode='w') as f:
                for line in ret:
                    f.write(line)




if __name__ == '__main__':

    #homedir = '/data/registration/Processed'
    homedir = os.path.join('/', 'data', 'registration', 'Test')
    registration = BahRegistration(homedir)
    registration.single_registration('CD00009-IS-BR-21.tif', sb_reslice_end=81)
