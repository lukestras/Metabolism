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
    #use np.polyfit(time, vals, )
    ax = plt.subplot(1,1,1)
    
    for col in plotted_cols:
        channel= re.search(r'(CH\s*\d+)',col)
        channel= channel[0]
        color = next(ax._get_lines.prop_cycler)['color']
        ax.plot(nm.ts_formatted_col,col, data=data, label=channel,color=color)
        #find @ 90% of max
        #print(channel)
        threshold_val = (
                data[col].iloc[0] - 0.1*(data[col].iloc[0]-data[col].min())) 
        """
        now slice from %90
        %90 is a (semi) arbitrary value
        """
        
        lin_df = data.iloc[data[data[col] < threshold_val].index[0]:]
#        ax.plot(lin_df[nm.ts_formatted_col].iloc[0],lin_df[col].iloc[0],
#                color=color,marker='o',linestyle='',
#                label= channel + 'linear')
        lin_reg = np.polyfit(lin_df[nm.ts_formatted_col],lin_df[col],1)
        lin_f = np.poly1d(lin_reg)
        lin_eq = '={0:0.3f}x + {1:0.0f}'.format(lin_reg[0],lin_reg[1])
        ax.plot(data[nm.ts_formatted_col], lin_f(data[nm.ts_formatted_col]), 
                linestyle='-.', color= color, label =channel + ' r' + lin_eq)
        #print(channel + ' ',lin_df[col].iloc[0])
        #print(channel + ' reg' + lin_eq)
        
    
    ax.set_title(name)
    ax.legend()
    plt.xlabel(nm.ts_formatted_col)
    plt.ylabel(nm.k_O2)
    plt.savefig(plot_dir + '/' + name + '.png', bbox_inches='tight',pad_inches=0,transparent=True)
    plt.show()
    