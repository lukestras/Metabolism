# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:27:07 2018

@author: Matthew
"""
import pandas as pd
import namespace as nm


def clean_data(data_in, calib_in):
    data = data_in.copy()
    """
    infer timestamps by getting timestamps - min(timestamps)
    """
    data[nm.ts_formatted_col] = data.loc[:,nm.ts_code_col] - data.loc[:,nm.ts_code_col].min()
    """
    Drop columns that aren't O2 related
    TODO: Remove this, better to fix poorly formatted cols
    """
    for word in nm.drop_col_words:
        data = data[data.columns.drop(list(data.filter(regex=word)))]
    
    #drop all na cols
    for col in data.columns:
        if data[col].isnull().all():
            data = data.drop(columns=col)    
    
    return data