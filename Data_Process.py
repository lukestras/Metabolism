# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:41:13 2018

@author: Matthew Strasiotto
"""
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt



input_dir = 'IN'
text_dir  = 'TXT'
input_excel = 'metabolism_imports.xlsx'

test_in = input_dir + '/' + input_excel
test_ws = None

out_dir = 'OUT'
plot_dir = out_dir + '/' + 'Plots'

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

test_cal  = pd.read_excel(test_in, sheet_name=test_ws, skiprows=calibration_start, nrows=calibration_len)
test_data = pd.read_excel(test_in, sheet_name=test_ws, skiprows=calibration_rows)

"""
Process your data so it's actually good
"""
for name, data in test_data.items():
    """
    infer timestamps by getting timestamps - min(timestamps)
    """
    data[ts_formatted_col] = data.loc[:,ts_code_col] - data.loc[:,ts_code_col].min()
    """
    Drop columns that aren't O2 related
    """
    for word in drop_col_words:
        data = data[data.columns.drop(list(data.filter(regex=word)))]
    
    test_data[name] = data

"""
Now make charts, find gradients
"""
for name, data in test_data.items():
    plotted_cols = list(data.filter(regex='O2'))
    
    #use np.polyfit(time, vals, )
    ax = plt.subplot(1,1,1)
    
    for col in plotted_cols:
        channel=re.search(r'(CH\s*\d+)',col)
        channel= channel[0]
        #print(channel)
        ax.plot(ts_formatted_col,col, data=data, label=channel)
    
    ax.set_title(name)
    ax.legend()
    plt.xlabel(ts_formatted_col)
    plt.ylabel('O2 [%Air Saturation]')
    plt.savefig(plot_dir + '/' + name + '.png', bbox_inches='tight',pad_inches=0,transparent=False)
    plt.show()
    