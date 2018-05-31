'''
	indicator.py

'''

import numpy
import pandas as pd
import matplotlib.pyplot as plt
from file_ops import *

def complete_qisummary(df, key_value=None):
    '''

    '''
    print 'preparing to generate full qi summary text'
    # qi_columns = ['QIDiabetes', 'QIDiabetesA1C', 'QIDiabetesFoot', 'QIDiabetesOphtho', 'QIDiabetesPneumovax', 'QIDiabetesReason',
    #           'QIMHReason1', 'QIMHReason2', 'QIMammo', 'QIMammoReason', 'QIMentalHealth1', 'QIMentalHealth2', 'QIMicroalbumin',
    #           'QIPHQ1', 'QIPHQ2', 'QIPHQ2Reason1', 'QIPHQ2Reason2', 'QIPap', 'QIPapReason']

    qi_columns = ['QIDiabetes', 'QIDiabetesA1C', 'QIDiabetesFoot', 'QIDiabetesOphtho', 'QIDiabetesPneumovax',
              'QIMammo', 'QIMentalHealth1', 'QIMentalHealth2', 'QIMicroalbumin',
              'QIPHQ1', 'QIPHQ2', 'QIPap']

    if key_value is None:

        for key_qi in qi_columns:
                if key_qi in df:
                    print df.groupby(key_qi).size()
                    plt.figure()
                    df.groupby(key_qi).size().plot(kind='bar')
                    plt.show()

                else:
                    print key_qi + ': no records found (assume 0)'

    else: 
        if key_value in df:
            print df.groupby(key_value).size()
        else:
            print key_value + ': No records found (assume 0)'

    return 


def temporal_distribution(df, ts_name = 'ts'):
	'''

	'''
	time_gb = df.groupby(df[ts_name].dt.weekofyear)
	plt.figure()
	time_gb.plot()
	plt.show()

# 	for key, item in time_gb:
# 		print time_gb.get_group(key), "\n\n"


def visits_paradigm(df):
	'''
	'''



if __name__ == "__main__":
    print 'testing indicator.py'
    path = 'data/QIdudes.csv'
    path2 = 'data/big_clinic_pull_5.13.csv'

    df_visits = returnDF(path2)
    df_visits['ts'] = pd.to_datetime((df_visits['DateTime']))
    visits_arbor = df_visits[df_visits['LocationAbbreviation'] == 'AFC']
    print visits_arbor.head(5)
    gb_apt_id = visits_arbor.groupby(visits_arbor['AppointmentID'])

    for key, item in gb_apt_id:
    	print gb_apt_id.get_group(key), '\n\n'

'''
    # open the QI csv into a pd dataframe
    df_QI = returnDF(path)
    df_QI['ts'] = pd.to_datetime((df_QI['VisitDate']))

    # write the QI csv to a pickle file just in case
    # write_to_pickle('df_QI',df_QI)

    arbor_data = df_QI[df_QI['LocationName'] == 'ARBOR']

    arbor_pivot = arbor_data.pivot_table(index='PatientNumber',columns='Note PropertyName',values='Note PropertyValue', aggfunc='first')
    # complete_qisummary(arbor_pivot)

    temporal_distribution(arbor_data)
'''

