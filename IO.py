# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:29:44 2018

@author: Matthew
"""
import pandas as pd
import namespace as nm
import pathlib

def write_out(data_dict, cal_dict, path):
    writer = pd.ExcelWriter(path)
    
    for name in data_dict:
        data_dict[name].to_excel(writer, name+nm.k_data)
        cal_dict[name].to_excel(writer, name+nm.k_cal)
    writer.save()
    return


"""
Read a single excel workbook, and return a dict of 2 dicts, CAL and DATA 
each entry in CAL corresponds to the calibration header of the sheet, 
and each entry in DATA corresponds to the data body of the named sheet.
"""
def read_excel(workbook_name):
    cal_tables = pd.read_excel(workbook_name, sheet_name=None, skiprows=nm.calibration_start, nrows=nm.calibration_len)
    data_tables = pd.read_excel(workbook_name, sheet_name=None, skiprows=nm.calibration_rows)
    out = {}
    out[nm.k_cal] = cal_tables
    out[nm.k_data] = data_tables
    
    return out

"""
Read a single text file, and return a dict of CAL, DATA
Will need to unpack the output of this a little to put it in a TYPE->Name hierachy
"""
def read_text(file_name):
    separator = r'\t'
    out = {}
    out[nm.k_cal] = pd.read_csv(file_name, sep=separator, skiprows=nm.calibration_start, nrows=nm.calibration_len)
    out[nm.k_data]= pd.read_csv(file_name, sep=separator, skiprows=nm.calibration_rows)
    return out

"""
Read everything in a folder into a dict of dicts of dframes
the hierachy is CAL/DATA->sheet_name
"""
def read_text_folder(folder_name, files_to_read=None):
    if not files_to_read:
        print("Uh oh")
        # placeholder, actually do everything unless a list is specified
    return