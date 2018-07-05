# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:41:13 2018

@author: Matthew Strasiotto
"""
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as collections


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
    
    for col in data.columns:
        if data[col].isnull().all():
            data = data.drop(columns=col)
    
    test_data[name] = data

"""
Now make charts, find gradients
"""
for name, data in test_data.items():
    plotted_cols = list(data.filter(regex='O2'))
    print(name)
    #use np.polyfit(time, vals, )
    ax = plt.subplot(1,1,1)
    
    for col in plotted_cols:
        channel=re.search(r'(CH\s*\d+)',col)
        channel= channel[0]
        color = next(ax._get_lines.prop_cycler)['color']
        ax.plot(ts_formatted_col,col, data=data, label=channel,color=color)
        #find @ 90% of max
        print(channel)
        threshold_val = (
                data[col].iloc[0] - 0.1*(data[col].iloc[0]-data[col].min())) 
        #now slice from %90
        lin_df = data.iloc[data[data[col] < threshold_val].index[0]:]
#        ax.plot(lin_df[ts_formatted_col].iloc[0],lin_df[col].iloc[0],
#                color=color,marker='o',linestyle='',
#                label= channel + 'linear')
        lin_reg = np.polyfit(lin_df[ts_formatted_col],lin_df[col],1)
        lin_f = np.poly1d(lin_reg)
        lin_eq = '={0:0.3f}x + {1:0.0f}'.format(lin_reg[0],lin_reg[1])
        ax.plot(data[ts_formatted_col], lin_f(data[ts_formatted_col]), 
                linestyle='-.', color= color, label =channel + ' r' + lin_eq)
        print(channel + ' ',lin_df[col].iloc[0])
        print(channel + ' reg' + lin_eq)
        
    
    ax.set_title(name)
    ax.legend()
    plt.xlabel(ts_formatted_col)
    plt.ylabel('O2 [%Air Saturation]')
    plt.savefig(plot_dir + '/' + name + '.png', bbox_inches='tight',pad_inches=0,transparent=True)
    plt.show()
    