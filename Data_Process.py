# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:41:13 2018

@author: Matthew Strasiotto
"""
import pandas as pd


input_dir = 'IN'
text_dir  = 'TXT'
input_excel = 'metabolism_imports.xlsx'

test_in = input_dir + '/' + input_excel

test_ws = 'New_1'

"""
Number of rows to be dropped to reach data
Note that this may change when working with raw txt, and also calibration data 
is PROBABLY of interest to analysis, so consider storing these headers 
someplace good
"""
calibration_rows = 13 

test_cal  = pd.read_excel(test_in, sheet_name=test_ws, skiprows=1, skipfooter=13)
test_data = pd.read_excel(test_in, sheet_name=test_ws, skiprows=13)