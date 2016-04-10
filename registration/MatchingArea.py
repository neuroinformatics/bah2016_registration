# -*- coding: utf-8 -*-

import sys
import os
import csv
from PIL import Image
from PIL import ImageStat

import RegistrationCommon


class MatchingArea:
    INTENSITY_THRESHOLD = 100
    SECTION_AREA_THRESHOLD = 10
    SECTION_AREA_BIAS = 10.0
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
        
        self.result_log = []

    def matching(self, filename):
        filename_base, filename_ext = os.path.splitext(filename)

        image_ish, slice_id = self._read_ish_file(filename_base)

        image_labeled = Image.open(self.labeled_filename % slice_id)
        print(self.labeled_filename % slice_id)

        labeled_intensity = self._matching_method_threashold(image_ish, image_labeled)

        self._write_result_file(filename_base, labeled_intensity)

        line = '%s' % filename_base
        for k, v in labeled_intensity.items():
            line += ', %f' % v
        self.result_log.append(line+'\n')


    def _matching_method_threashold(self, image_ish, image_labeled):
        # Initialize data
        data_ish = image_ish.getdata()
        data_labeled = image_labeled.getdata()

        labeled_area = {}
        labeled_intensity = {}
        labeled_intensity_per_area = {}

        for i in range(self.N_LABELED_AREA):
            labeled_area[i] = 0
            labeled_intensity[i] = 0
            labeled_intensity_per_area[i] = 0.0


        # Process
        for val_ish, val_labeled in zip(data_ish, data_labeled):
            labeled_area[val_labeled] += 1
            if val_labeled != 0 and val_ish < self.INTENSITY_THRESHOLD:
                labeled_intensity[val_labeled] += 1


        # Normalize intensity by volume
        for i in range(self.N_LABELED_AREA):
            if labeled_area[i] > self.SECTION_AREA_THRESHOLD:
                labeled_intensity_per_area[i] = float(labeled_intensity[i]) / (labeled_area[i] + self.SECTION_AREA_BIAS)


        #return labeled_intensity
        return labeled_intensity_per_area


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


    def _write_result_file(self, filename_base, labeled_intensity):
        result_filename = os.path.join(self.result_dir, filename_base+'.txt')
        with open(result_filename, 'w') as f:
            for k, v in labeled_intensity.items():
                f.write('%d, %f\n' % (k, v))

    def write_log(self, filename):
        with open(os.path.join(self.homedir, filename), 'w') as f:
            f.writelines(self.result_log)


if __name__ == '__main__':

    filelistname = os.path.join('/', 'data', 'registration', 'Test', 'filelist_all0.txt')
    filelist = RegistrationCommon.read_filelist(filelistname)

    matchingarea = MatchingArea()

    for filename in filelist:
        matchingarea.matching(filename)

    matchingarea.write_log('intensity_all.txt')

