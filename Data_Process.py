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
import namespace as nm
import work
import IO

input_dir = 'IN'
text_dir  = 'TXT'
input_excel = 'metabolism_imports.xlsx'

test_in = input_dir + '/' + input_excel
test_ws = None

out_dir = 'OUT'
plot_dir = out_dir + '/' + 'Plots'



 

test_cal  = pd.read_excel(test_in, sheet_name=test_ws, skiprows=nm.calibration_start, nrows=nm.calibration_len)
test_data = pd.read_excel(test_in, sheet_name=test_ws, skiprows=nm.calibration_rows)

"""
Process your data so it's actually good
"""
for name, data in test_data.items():
    
    test_data[name] = work.clean_data(data)
    test_cal[name]  = work.clean_cal(test_cal[name])

"""
Now make charts, find gradients
"""
for name, data in test_data.items():
    plotted_cols = list(data.filter(regex='O2'))
    print(name)
    
    ax = plt.subplot(1,1,1)
    
    for col in plotted_cols:
        match   = re.search(nm.g_channel+nm.g_channel_n, col)
        ch      = match.group(nm.k_channel)
        ch_num  = match.group(nm.k_channel_n)
        channel = ch+ch_num
        color = next(ax._get_lines.prop_cycler)['color']
        ax.plot(nm.ts_formatted_col,col, data=data, label=channel,color=color)
        lin_reg = work.find_gradient(data, nm.ts_formatted_col, col)
        lin_f = np.poly1d(lin_reg)
        lin_eq = '={0:0.3f}x + {1:0.0f}'.format(lin_reg[0],lin_reg[1])
        
        test_cal[name].loc[test_cal[name].loc[:,nm.k_channel_n] == ch_num, nm.k_O2 + nm.kw_grad] = lin_reg[0]
        test_cal[name].loc[test_cal[name].loc[:,nm.k_channel_n] == ch_num, nm.k_O2 + nm.kw_offset]= lin_reg[1]   
        ax.plot(data[nm.ts_formatted_col], lin_f(data[nm.ts_formatted_col]), 
                linestyle='-.', color= color, label =channel + ' r' + lin_eq)
        
        
        
    
    ax.set_title(name)
    ax.legend()
    plt.xlabel(nm.ts_formatted_col)
    plt.ylabel(nm.k_O2)
    plt.savefig(plot_dir + '/' + name + '.png', bbox_inches='tight',pad_inches=0,transparent=True)
    plt.show()

IO.write_out(test_data,test_cal, out_dir + '/' + 'data.xlsx')    