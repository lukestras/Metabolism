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

"""
Capturing Groups
"""
k_bad       = r'bad'
k_channel   = r'channel'
k_channel_n = r'channel_n'
k_unit      = r'unit'

g_bad       = r'(?P<' +k_bad+ r'>\S+ *,)\s*'
g_channel   = r'(?P<' +k_channel+ r'>CH)\s*'
g_channel_n = r'(?P<' +k_channel_n+ r'>\d+)'
g_unit      = r'(?P<' +k_unit+ r'>\s+.*)'