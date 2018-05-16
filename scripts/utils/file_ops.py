'''
	file_ops.py

'''
import numpy
import pandas as pd
import matplotlib as plt
import csv

def returnDF(csv_path):
    '''
    input: 
    	* the path to the csv file 

    output:
    	* a pandas dataframe


    This is the function wrapper that we're going to use to avoid a bug in Pandas dataframe generation 
    from csv. (the real reason is because there are some messy characters in the csv that throw errors 
    within the pandas.read_csv function, but these errors don't seem to show up with python's builtin csv package)
    '''

    print 'preparing to open csv at:', csv_path
    row_list = []
    with open(csv_path, 'rb') as f:
        reader = csv.DictReader(f)
        for c, row in enumerate(reader):
            #if c < 10:
             #   print row
            #print c
            
            row_list.append(row)

    data_df = pd.DataFrame(row_list)
    print 'done preparing dataframe'

    return data_df
    