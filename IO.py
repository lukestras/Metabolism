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
    separator = '\t'
    out = {}
    out[nm.k_cal] = pd.read_csv(file_name, sep=separator, skiprows=nm.calibration_start, nrows=nm.calibration_len)
    out[nm.k_data]= pd.read_csv(file_name, sep=separator, skiprows=nm.calibration_rows)
    return out

"""
Read everything in a folder into a dict of dicts of dframes
the hierachy is CAL/DATA->sheet_name
this is consistent with the output of the read_excel function
accepts a folder name, and a list of files within to read
if given just a folder name, will try to read all text files within
"""
def read_text_folder(folder_name, files_to_read=None):
    out = {}
    out[nm.k_cal] = {}
    out[nm.k_data] = {}
    
    folder = pathlib.Path(folder_name)
    if not folder.is_dir():
        print("Invalid directory name!")
        return None
    
    # if not specified a list
    if not files_to_read:
        files_to_read = []
        # iterate over the contents of the directory, and add any files 
        # that end in ".txt" to the list
        for child in folder.iterdir():
            if child.is_file() and '.txt' == child.suffix:
                files_to_read += [child]
                # print("Gonna read " + child.name)
                
    #print("Files to read:\t", files_to_read)
    for filename in files_to_read:
        #print(filename)
        single_file_dict = read_text(filename)
        out[nm.k_cal][filename.name] = single_file_dict[nm.k_cal]
        out[nm.k_data][filename.name] = single_file_dict[nm.k_data]
    return out