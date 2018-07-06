# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:27:07 2018

@author: Matthew
"""
import pandas as pd
import namespace as nm
import re

def clean_data(data_in, calib_in):
    data = data_in.copy()
    """
    infer timestamps by getting timestamps - min(timestamps)
    """
    data[nm.ts_formatted_col] = data.loc[:,nm.ts_code_col] - data.loc[:,nm.ts_code_col].min()
    
    col_dict = {}
    
    for col in data.columns:
        col_dict[col] = col
        match = re.search(r'(?P<bad>\S+ *,)\s*(?P<channel>CH)\s*(?P<channel_n>\d+)(?P<unit>\s+.*)',col_dict[col])
        if match:
            col_dict[col] = match.group('channel') + match.group('channel_n') + match.group('unit')
    
    data = data.rename(col_dict, axis='columns')
    #drop all na cols
    for col in data.columns:
        if data[col].isnull().all():
            data = data.drop(columns=col)    
    
    return data