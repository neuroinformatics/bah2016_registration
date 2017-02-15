# -*- coding: utf-8 -*-


def read_file_list(file_list_name):
    with open(file_list_name, mode='r') as f:
        file_list = f.readlines()
        
    file_list = [name.rstrip() for name in file_list]
    return file_list
