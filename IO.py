# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:29:44 2018

@author: Matthew
"""
import pandas as pd
import namespace as nm

def write_out(data_dict, cal_dict, path):
    writer = pd.ExcelWriter(path)
    
    for name in data_dict:
        data_dict[name].to_excel(writer, name+nm.k_data)
        cal_dict[name].to_excel(writer, name+nm.k_cal)
    writer.save()
    return