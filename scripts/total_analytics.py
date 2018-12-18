'''
	total_analytics.py

'''

import numpy
import pandas as pd 
import sys
import argparse
import csv 

from utils.file_ops import * 
from datetime import datetime


def time_filter(t1, t2, df):
	'''
		note: datetime accepts numerical tuples of form (year, mon, day)
	'''

	bound1 = datetime(*t1)
	bound2 = datetime(*t2)
	
	return df[bound1:bound2]


def process_qi_csv(path_to_qi_csv):
	'''
	'''

	print '---------------------------'
	print 'processing visits dataframe'

	df_qi= returnDF(path_to_qi_csv)
	df_qi['VisitDateTimeTS'] = pd.to_datetime((df_qi['VisitDate']))
	df_qi.index = df_qi['VisitDateTimeTS']
	df_qi = df_qi.iloc[::-1]
	del df_qi['VisitDate']

	print df_qi['LocationName'].describe()

	arbor_qi = df_qi[df_qi['LocationName'] == 'ARBOR']
	pfc_qi = df_qi[df_qi['LocationName'] != 'ARBOR']

	print '-------------------------------'
	print 'done processing visits dataframe'

	return {'arbor':arbor_qi, 'pfc':pfc_qi}


def process_qi_csv_preselect(path_to_qi_csv):
	'''
	'''

	print '--------------------------------'
	print 'processing visits dataframe'

	df_qi= returnDF(path_to_qi_csv)
	df_qi['VisitDateTimeTS'] = pd.to_datetime((df_qi['VisitDate']))
	df_qi.index = df_qi['VisitDateTimeTS']
	#df_qi = df_qi.iloc[::-1]
	del df_qi['VisitDate']

	print df_qi.describe()

	return df_qi


def process_visits_csv(path_to_flow_csv):
	'''
	'''

	print '-----------------------------'
	print 'preparing to tabulate visits'

	df_visits = returnDF(path_to_flow_csv)
	df_qi['VisitDateTimeTS'] = pd.to_datetime((df_qi['VisitDate']))
	df_qi.index = df_qi['VisitDateTimeTS']
	df_qi = df_qi.iloc[::-1]

	# ok fuck there are so many steps to process this data

	# -1) read in the shit 
	df_visits = returnDF(path_to_flow_csv)


	# 0) set up the index on time last modified
	df_visits['VisitDateTimeTS'] = pd.to_datetime((df_visits['VisitDateTime']))
	df_visits['DateFirstKnownTS'] = pd.to_datetime((df_visits['DateFirstKnown']))
	df_visits.index = df_visits['VisitDateTimeTS']
	#df_visits = df_visits.iloc[::-1]
	del df_visits['DateFirstKnown']
	del df_visits['VisitDateTime']
	del df_visits['MRN']

	df_visits = df_visits[df_visits['LocationAbbreviation'] != 'TEST']
	arbor_visits = df_visits[df_visits['LocationAbbreviation'] == 'AFC']
	pfc_visits = df_visits[df_visits['LocationAbbreviation'] != 'AFC']

	print df_visits.groupby('LocationAbbreviation').size()


	# visit types that we're looking at 
	'''

	ARBOR GENERAL VISIT, ARBOR FOLLOW-UP VISIT, ARBOR MENTAL HEALTH, ARBOR MSK, ARBOR NEUROLOGY, ARBOR WOMEN'S HEALTH, ARBOR CARDIOLOGY, ARBOR DERMATOLOGY, ARBOR OPHTHALMOLOGY

	PFC NEW PATIENT VISIT, PFC FOLLOW UP VISIT, PFC HEP CLINIC, PFC FAST TRACK, PFC WOMEN'S CLINIC, PFC DERMATOLOGY, PFC OPTHALMOLOGY, 
	'''

	# 1) we need to chop off the really old patients, like pre-2016 

	# 2) separate the patients into AFC and PFC 

	# 3) identify general clinic visits

	# 4-1) group by id? and identify the first time visits/subsequent visits

	# 4-2) count first time visits per month



def qisummary(df, mapping, key_value=None):
	'''

	'''
	print '------------------------------------------'
	print 'preparing to generate full qi summary text'

	# qi_columns = ['QIDiabetes', 'QIDiabetesA1C', 'QIDiabetesFoot', 'QIDiabetesOphtho', 'QIDiabetesPneumovax', 'QIDiabetesReason',
	#           'QIMHReason1', 'QIMHReason2', 'QIMammo', 'QIMammoReason', 'QIMentalHealth1', 'QIMentalHealth2', 'QIMicroalbumin',
	#           'QIPHQ1', 'QIPHQ2', 'QIPHQ2Reason1', 'QIPHQ2Reason2', 'QIPap', 'QIPapReason']

	qi_columns = ['QIDiabetes', 'QIDiabetesA1C', 'QIDiabetesFoot', 'QIDiabetesOphtho', 'QIDiabetesPneumovax',
			  'QIMammo', 'QIMentalHealth1', 'QIMentalHealth2', 'QIMicroalbumin',
			  'QIPHQ1', 'QIPHQ2', 'QIPap']

	response_dict = {key:{} for key in qi_columns}
	
	if key_value is None:

		for key_qi in qi_columns:
				if key_qi in df:
					#print df.groupby(key_qi).size()
					print key_qi,
					grouped = df.groupby(key_qi)
					for response_key, mapped_response in mapping[key_qi].iteritems():
						if response_key in grouped.groups:
							response_dict[key_qi][mapped_response] = len(grouped.groups[response_key])
						else:
							response_dict[key_qi][mapped_response] = 0
#                     for p in grouped.groups:
#                         print p, 'has', len(grouped.groups[p])
#                         response_dict[key_qi][mapping[key_qi][p]] = len(grouped.groups[p])
					df.groupby(key_qi).size()

				else:
					print key_qi + ': no records found (assume 0)'
					for response_key, mapped_response in mapping[key_qi].iteritems():
						response_dict[key_qi][mapped_response] = 0

	else: 
		if key_value in df:
			print df.groupby(key_value).size()
		else:
			print key_value + ': No records found (assume 0)'

	print '--------------------------'
	print 'done performing qi summary'
	return response_dict


def qi_extractor(df, period='mom', keys=None):
	'''
		input:
			* df -- the unpivoted table 
			* period (optional): the timeframe we should include in each pivot 
			* keys (optional): the qi value(s) we should examine 
		output:
			* response_dict: dictionary that provides mapping from key to a dict 
			 of interpretable response -> the number of responses 
			 in form: {key: {mapped_response: list of num responses}} 
	'''
	
	print '------------------------------------------'
	print 'preparing to generate full qi summary text'

	print df.head()
	# qi keys 
	qi_columns = ['QIDiabetes', 'QIDiabetesA1C', 'QIDiabetesFoot', 'QIDiabetesOphtho', 'QIDiabetesPneumovax',
			  'QIMammo', 'QIMentalHealth1', 'QIMentalHealth2', 'QIMicroalbumin',
			  'QIPHQ1', 'QIPHQ2', 'QIPap']

	# response mapping dict
	interpretation = {
					'QIDiabetes': {'Yes': 'Positive', 'No': 'Negative', 'Not Questioned': 'Not Questioned'},
					'QIDiabetesA1C': {'True': 'Checked', 'False':'Not checked'},
					'QIDiabetesFoot': {'True':'Checked', 'False':'Not checked'},
					'QIDiabetesOphtho': {'True':'Referred', 'False':'Not referred'},
					'QIDiabetesPneumovax': {'True':'Received', 'False':'Not received'},
					'QIMammo': {'Yes':'Mammography given', 'No':'Mammography not given', 'Not Indicated':'Mamm not indicated', 'Already Received':'Already Received'},
					'QIMentalHealth1': {'Yes':'Yes', 'No': 'No'},
					'QIMentalHealth2':{'Yes':'Yes', 'No':'No'},
					'QIPHQ1': {'Yes':'Anhedonia Positive', 'No':'Anhedonia Negative', 'Not Questioned':'Not Questioned'},
					'QIPHQ2':{'Yes': 'Hopeless Mood Positive', 'No': 'Hopeless Mood Negative', 'Not Questioned':'Not Questioned'},
					'QIPap': {'Yes':'Pap given', 'No':'Pap not given', 'Not Indicated':'Pap not indicated', 'Already Received':'Already Received'},
					'QIMicroalbumin': {'True':'Checked', 'False':'Not checked'}

					}

	total_responses = {
					key_qi:{ 
					mapped_response:[] for response_key, mapped_response in interpretation[key_qi].iteritems() 
						} 
					for key_qi in qi_columns 
					}
	
	# PIVOT
	
	if period == 'mom':
		months = [val for val in range(1, 13)]
		years = [ 2018]
		time_points = []
		
		for year in years:
			for begin_month in months:
				print year, begin_month

				tp1 = (year, begin_month, 1)
				tp2 = ()

				if begin_month == 12:
					tp2 = (year+1, 1, 1)
				else:
					tp2 = (year, begin_month+1, 1)

				filtered = time_filter(tp1,tp2, df)

				if filtered.values.shape[0] == 0:
					print 'No QI data between these time points:', tp1, tp2
					continue

				else:
					pivoted = filtered.pivot_table( index='PatientNumber', columns='Note PropertyName', values='Note PropertyValue', aggfunc='first')
					summ = qisummary(pivoted, interpretation)
					for key_qi, response_dict in summ.iteritems():
						for mapped_key, num_patients in response_dict.iteritems():
							total_responses[key_qi][mapped_key].append(num_patients)
							
					time_points.append(str(tp1[1]) + '/' + str(tp1[0]))

	return (total_responses, time_points)
				

def fuse_diabetes_df(results_dict):
	'''
		input:
			* big df 
		output:
			* smaller df with diabetes stuff fused into one df 
	'''
	diabetes_key = 'QIDiabetes'
	qi_keys = ['QIDiabetesA1C', 'QIDiabetesFoot', 'QIDiabetesOphtho', 'QIDiabetesPneumovax', 'QIMicroalbumin']

	locations = ['arbor', 'pfc']

	fused_dict = {location:[] for location in locations}

	for location in locations: 
		location_specific_df = results_dict[location]
		base_df = location_specific_df[diabetes_key]
		del base_df['Negative']
		del base_df['Not Questioned']
		base_df.rename(columns={'Positive':'Total Diabetic'}, inplace=True)

		for qi_key in qi_keys:
			sub_key = None
			if 'Checked' in location_specific_df[qi_key].columns.values:
				sub_key = 'Checked'
			elif 'Referred' in location_specific_df[qi_key].columns.values:
				sub_key = 'Referred'
			elif 'Received' in location_specific_df[qi_key].columns.values:
				sub_key = 'Received'

			base_df[qi_key] = location_specific_df[qi_key][sub_key]


		fused_dict[location] = base_df

	write_to_pickle('diabetes_fused', fused_dict)




def QI_processing(path_to_qi_csv):
	'''
		ok so the goal should be to start from 

		input: 
			* path to the qi csv
			* specs on time interval, which qi selectors

		in order to get to some pickle(s) that contain 
			* the way people respond for every one of the QI questions
	'''

	
	qi_df = process_qi_csv_preselect(path_to_qi_csv)

	grouped_data, time_points = qi_extractor(qi_df)
	extracted_qi_df_dict = {key_qi:pd.DataFrame(mom, index = time_points) for key_qi, mom in grouped_data.iteritems()}
	for key_qi, df in extracted_qi_df_dict.iteritems():
		df.index.name = 'time_point'


	return (extracted_qi_df_dict, time_points)

def parse_command_line(args):
	'''

	'''
	
	print 'parsing command line'

	parser = argparse.ArgumentParser(description='lol')
	parser.add_argument('--raw_arbor', action="store", type=str)
	parser.add_argument('--raw_pfc', action="store", type=str)
	
	args = vars(parser.parse_args())

	return args

def main():

	args = parse_command_line(sys.argv)

	# path_to_qi_csv = "data/QIdudes.csv"
	# path_to_flow_csv = 

	# path_to_qi_csv_arbor = "data/QI_summer_2018_raw_arbor.csv"
	# path_to_qi_csv_pfc = "data/QI_summer_2018_raw_pfc.csv"

	path_to_qi_csv_arbor = args['raw_arbor']
	path_to_qi_csv_pfc = args['raw_pfc']

	extracted_arbor, _ = QI_processing(path_to_qi_csv_arbor)
	extracted_pfc, _ = QI_processing(path_to_qi_csv_pfc)

	results_dict = {'arbor': extracted_arbor, 'pfc': extracted_pfc}
	write_to_pickle('qi_results_dict_mom', results_dict)

	fuse_diabetes_df(results_dict)



if __name__ == "__main__":
	main()

