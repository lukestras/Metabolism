# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:27:07 2018

@author: Matthew
"""
import pandas as pd
import namespace as nm
import re

def clean_data(data_in):
    data = data_in.copy()
    """
    infer timestamps by getting timestamps - min(timestamps)
    """
    data[nm.ts_formatted_col] = data.loc[:,nm.ts_code_col] - data.loc[:,nm.ts_code_col].min()
    
    col_dict = {}
    
    for col in data.columns:
        col_dict[col] = col
        match = re.search(nm.g_bad+nm.g_channel+nm.g_channel_n+nm.g_unit,col_dict[col])
        if match:
            col_dict[col] = match.group(nm.k_channel) + match.group(nm.k_channel_n) + match.group(nm.k_unit)
    
    data = data.rename(col_dict, axis='columns')
    #drop all na cols
    for col in data.columns:
        if data[col].isnull().all():
            data = data.drop(columns=col)    
    
    return data

def clean_cal(data_in):
    data = data_in.copy()
    
    for col in data.columns:
        if data[col].isnull().all():
            data = data.drop(columns=col)
    
    return data