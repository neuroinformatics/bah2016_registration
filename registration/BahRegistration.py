# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import matplotlib
import csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class BahRegistration:

    def __init__(self, homedir=None, reg_program=None):

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
        self.registration_metric_fig = os.path.join(homedir, 'metric_fig')
        
        if not os.path.exists(self.registration_in):
            sys.exit('Error : %s not found.' % self.registration_in)

        # output dirs
        # TODO: this mkdir methods is not good for parallelization
        if not os.path.exists(self.registration_out):
            os.mkdir(self.registration_out)
        if not os.path.exists(self.registration_log):
            os.mkdir(self.registration_log)
        if not os.path.exists(self.registration_metric):
            os.mkdir(self.registration_metric)
        if not os.path.exists(self.registration_metric_fig):
            os.mkdir(self.registration_metric_fig)

        # result data
        self.result_metric = None
        self.filename_base = None
    
    def single_registration(self, filename, sb_reslice_start=80, sb_reslice_end=82):

        filename_base, filename_ext = os.path.splitext(filename)
        self.filename_base = filename_base
        outdir = os.path.join(self.registration_out, filename_base)
        logdir = os.path.join(self.registration_log, filename_base)
        metricfilename = os.path.join(self.registration_metric, filename_base+'.txt')
        self.result_metric = {}

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
            print(cmd)

            ret = subprocess.check_output(cmd)
            result = ret.split("\n")

            with open(logfilename, mode='w') as f:
                for line in result:
                    f.write(line)
                    if 'Metric value' in line:
                        line_split = line.split("=")
                        self.result_metric[i] = line_split[1]

        print(self.result_metric)
        with open(metricfilename, mode='w') as f:
            for k, v in self.result_metric.items():
                f.write(str(k)+', '+v+'\n')

        return self.result_metric

    def draw_metric_graph(self, filename_base=None):
        if filename_base is None:
            filename_base = self.filename_base
        filename = os.path.join(self.homedir, self.registration_metric_fig, filename_base+'.png')

        if self.result_metric is None:
            sys.exit('Error : need to registration first.')

        data_x = []
        data_y = []
        range_min = 1000
        range_max = 0
        for k, v in self.result_metric.items():
            if k < range_min:
                range_min = k
            if k > range_max:
                range_max = k

        for i in range(range_min, range_max+1):
            data_x.append(i)
            data_y.append(self.result_metric[i])
            
        plt.plot(data_x, data_y, 'r.-')
        plt.title('Metric Value of %s' % filename_base)
        plt.xlabel('Slice Number')
        plt.ylabel('Metric Value')
        plt.grid(True)
        plt.savefig(filename)
        plt.close()

    def draw_metric_graph_from_file(self, filename_base):
        self.result_metric = {}
        filename = os.path.join(self.homedir, self.registration_metric, filename_base+'.txt')
        with open(filename, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.result_metric[int(row[0])] = float(row[1])

        print(self.result_metric)
        self.draw_metric_graph(filename_base=filename_base)

    def intensity_segmentation(self, filename, slice_no):
        pass
        

if __name__ == '__main__':

    # homedir = '/data/registration/Processed'
    homedir = os.path.join('/', 'data', 'registration', 'Test')
    reg = BahRegistration(homedir)
    # reg.single_registration('CD00009-IS-BR-21.tif', sb_reslice_end=83)
    reg.draw_metric_graph_from_file('CD00009-IS-BR-21')

