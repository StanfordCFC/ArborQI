'''
	file_ops.py

'''
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import pickle
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
    with open(csv_path, 'rU') as f:
        reader = csv.DictReader(f)
        for c, row in enumerate(reader):
            #if c < 10:
             #   print row
            #print c
            
            row_list.append(row)

    data_df = pd.DataFrame(row_list)
    print 'done preparing dataframe'

    return data_df
    


def write_to_pickle(name, obj):
    '''
        Write object of specified name to a pickle file 
    '''
    path = 'pickles/' + name + '.pkl'
    file = open(path, 'wb')
    pickle.dump(obj, file)
    file.close()


def read_from_file(name):
    '''
        Return loaded object given by input name
    '''
    path = 'pickles/' + name + '.pkl'
    file = open(path, 'rb')
    new_obj = pickle.load(file)
    file.close()

    return new_obj


if __name__ == "__main__":
    print 'testing??'
    path = 'data/QIdudes.csv'
    df_QI = returnDF(path)
    arbor_data = df_QI[df_QI['LocationName'] == 'ARBOR']
    arbor_pivot = arbor_data.pivot_table(index='PatientNumber',columns='Note PropertyName',values='Note PropertyValue', aggfunc='first')
    complete_qisummary(arbor_pivot)


