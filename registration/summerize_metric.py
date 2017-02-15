# -*- coding: utf-8 -*-

import os
import csv
import RegistrationCommon

if __name__ == '__main__':
    def main():
        home_dir = '/data/registration/Processed20170212/'
        file_list_name = os.path.join(home_dir, 'filelist_2810.txt')
        summarize_file = os.path.join(home_dir, 'summarize_metric.txt')
        metric_path = os.path.join(home_dir, 'metric')

        best_slice_list = []

        for file_name in RegistrationCommon.read_file_list(file_list_name):

            with open(os.path.join(metric_path, os.path.splitext(file_name)[0] + '.txt'), 'r') as f:
                reader = csv.reader(f)
                metric_list = []
                for row in reader:
                    metric_list.append({'slice_no': row[0], 'metric_value': row[1]})

                min_value = metric_list[0]['metric_value']
                min_slice = metric_list[0]['slice_no']
                for metric in metric_list:
                    if min_value > metric['metric_value']:
                        min_value = metric['metric_value']
                        min_slice = metric['slice_no']

            best_slice_list.append({'file_name': file_name, 'slice_no': min_slice, 'metric_value': min_value})

        with open(summarize_file, 'w') as f:
            for best_slice in best_slice_list:
                f.write("%s, %s, %s\n" % (best_slice['file_name'], best_slice['slice_no'], best_slice['metric_value']))


    main()
