# -*- coding: utf-8 -*-

import subprocess
import os
import sys

class BahRegistration:

    def __init__(self,
                 homedir = None,
                 reg_program = None
                 ):

        if homedir is None:
            homedir = os.path.join('/', 'data', 'registration', 'Processed')
        if not os.path.exists(homedir):
            sys.exit('Error : %s not found.' % homedir)

        if reg_program is None:
            reg_program = '/share/apps/registration/itk/ImageRegistration/ImageRegistration9'
        if not os.path.exists(reg_program):
            sys.exit('Error : %s not found.' % reg_program)


        self.homedir = homedir
        self.reg_program = reg_program
        self.sbfile_base = os.path.join(homedir, 'SB_bin', 'Reslice_WHS_0.6.1_Labels_fixed_bin%04d.tif')
        self.registration_in = os.path.join(homedir, 'work3')
        self.registration_out = os.path.join(homedir, 'work4')
        self.registration_log = os.path.join(homedir,'log4')
        self.registration_metric = os.path.join(homedir, 'metric')
        
        if not os.path.exists(self.registration_in):
            sys.exit('Error : %s not found.' % self.registration_in)

        
        # output dirs
        if not os.path.exists(self.registration_out):
            os.mkdir(self.registration_out)
        if not os.path.exists(self.registration_log):
            os.mkdir(self.registration_log)
        if not os.path.exists(self.registration_metric):
            os.mkdir(self.registration_metric)

    
    def single_registration(self, filename,
                            sb_reslice_start=80, sb_reslice_end=121):

        filename_base, filename_ext = os.path.splitext(filename)
        outdir = os.path.join(self.registration_out, filename_base)
        logdir = os.path.join(self.registration_log, filename_base)
        metricfilename = os.path.join(self.registration_metric, filename_base+'.txt')
        result_metric = {}

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        if not os.path.exists(logdir):
            os.mkdir(logdir)

        for i in range(sb_reslice_start, sb_reslice_end):
            sbfile = self.sbfile_base % i
            inputfile = os.path.join(self.registration_in, filename)
            outputfile = os.path.join(outdir, ('%04d.tif' % i))
            logfilename = os.path.join(logdir, ('%04d.log' % i))
            
            cmd = [self.reg_program, sbfile, inputfile, outputfile]
            print cmd

            ret = subprocess.check_output(cmd)
            result = ret.split('\n')

            with open(logfilename, mode='w') as f:
                for line in result:
                    f.write(line)
                    if 'Metric value' in line:
                        line_split = line.split('=')
                        result_metric[i] = line_split[1]

        with open(metricfilename, mode='w') as f:
            for k, v in result_metric.items():
                f.write(str(k)+', '+v)

        return result_metric

    


if __name__ == '__main__':

    #homedir = '/data/registration/Processed'
    homedir = os.path.join('/', 'data', 'registration', 'Test')
    registration = BahRegistration(homedir)
    registration.single_registration('CD00009-IS-BR-21.tif', sb_reslice_end=81)
