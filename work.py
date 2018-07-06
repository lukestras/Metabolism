# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:27:07 2018

@author: Matthew
"""
import pandas as pd
import namespace as nm
import re
import numpy as np
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
    
    info = data[nm.cal_in_param_channel].str.extract(nm.g_bad+nm.g_channel+nm.g_channel_n)
    info[nm.k_bad] = info[nm.k_bad].str.replace(r'\s*,','')
    info = info.drop(columns=nm.k_channel)
    
    data = data.join(info)
    return data

def find_gradient(data_in, x_col, y_col, x_lo=None, x_hi=None):
    data = data_in.copy()

    """
    Unless otherwise specified, slice from 90% to %10
    """
    y_range = data[y_col].iloc[0]-data[y_col].min()
    thresh_range = 0.1*y_range
    hi_thresh_val = data[y_col].iloc[0] - thresh_range
    lo_thresh_val = data[y_col].min() + thresh_range/2
    
    lin_df = data.iloc[data[data[y_col] < hi_thresh_val].index[0]:]
    if x_hi:    
        lin_df = data.iloc[data[data[x_col] <= x_hi].index[0]:] 
    
    if x_lo:
        lin_df = lin_df.iloc[:len(lin_df[lin_df[x_col] >= x_lo].index)]
    else:
        lin_df = lin_df.iloc[:len(lin_df[lin_df[y_col] > lo_thresh_val].index)]
    
    lin_reg = np.polyfit(lin_df[x_col],lin_df[y_col],1)
    
    return lin_reg