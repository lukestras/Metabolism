# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:25:28 2018

@author: Matthew Strasiotto
"""

ts_code_col = 'Time stamp code'
ts_formatted_col = 'Time (s)'

drop_col_words = [r'temp', r'phase']

"""
Number of rows to be dropped to reach data
Note that this may change when working with raw txt, and also calibration data 
is PROBABLY of interest to analysis, so consider storing these headers 
someplace good
"""
calibration_rows = 13
calibration_start = 6
calibration_len   = 4

cal_key = 'CAL'
data_key = 'DATA'