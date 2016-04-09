# -*- coding: utf-8 -*-

import sys
import os
import csv
from PIL import Image
from PIL import ImageStat

class MatchingArea:
    INTENSITY_THRESHOLD = 10
    SECTION_AREA_THREASHOLD = 10
    SECTION_AREA_BIAS = 40
    N_LABELED_AREA = 40
    
    
    def __init__(self, homedir=None,  labeled_filename=None):

        if homedir is None:
            homedir = os.path.join('/', 'data', 'registration', 'Test')
            self.homedir = homedir
        if not os.path.exists(homedir):
            sys.exit('Error : %s not found.' % homedir)

        if labeled_filename is None:
            self.labeled_filename = os.path.join(homedir, 'reslice_labeled_8bit', 'reslice_labeled%04d.tif')


        self.ish_dir = os.path.join(homedir, 'work4')
        self.metric_dir = os.path.join(homedir, 'metric')

        self.result_dir = os.path.join(homedir, 'area')
        if not os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)
        

    def matching(self, filename_base):
        image_ish, slice_id = self._read_ish_file(filename_base)

        image_labeled = Image.open(self.labeled_filename % slice_id)
        print(self.labeled_filename % slice_id)

        labeled_area = self._matching_method_threashold(image_ish, image_labeled)

        self._write_result_file(filename_base, labeled_area)

        def showinfo(x):
            print x.format, x.size, x.mode

        showinfo(image_ish)
        showinfo(image_labeled)


    def _matching_method_threashold(self, image_ish, image_labeled):
        # Initialize data
        data_ish = image_ish.getdata()
        data_labeled = image_labeled.getdata()

        labeled_area = {}
        for i in range(self.N_LABELED_AREA):
            labeled_area[i] = 0

        for val_ish, val_labeled in zip(data_ish, data_labeled):
            labeled_area[val_labeled] += 1

        return labeled_area


    def _read_ish_file(self, filename_base):

        metric = {}
        metric_filename = os.path.join(self.metric_dir, filename_base+'.txt')

        with open(metric_filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                metric[int(row[0])] = float(row[1])
                
        min_slice_id = min(metric.items(), key=lambda x:x[1])[0]
        #print min_slice
        regist_filename = os.path.join(self.ish_dir, filename_base, ('%04d.tif' % min_slice_id))
        print regist_filename

        return Image.open(regist_filename), min_slice_id



    def _write_result_file(self, filename_base, labeled_area):
        result_filename = os.path.join(self.result_dir, filename_base+'.txt')
        with open(result_filename, 'w') as f:
            for k, v in labeled_area.items():
                f.write('%d, %d\n' % (k, v))



if __name__ == '__main__':

    matchingarea = MatchingArea()
    matchingarea.matching('CD00791-IS-BR-21')

