__author__ = 'Shi Fan'
import pandas as pd, numpy as np

if __name__=='__main__':
	# dataset can be downloaded from here
	# https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
	# set filter: "Agency is DOHMH" and "Location Type contains Restaurant"
	# click "Export" and "Download as CSV"
	df = pd.read_csv('../input/311_DOHMH_Restaurant.csv')
	# cleaning data
	df = df[df['Incident Zip']!='NY']
	df['Incident Zip'] = df['Incident Zip'].astype(float)
	df = df.dropna(subset=['Incident Zip'])
	df['Incident Zip'] = df['Incident Zip'].astype(int)
	df = df[(df['Incident Zip']>10000) & (df['Incident Zip']<20000)]
	# feature engineering
	comp_types = ['Total Complaints','Food Establishment', 'Food Poisoning', 'Smoking']
	cols = ['num_complaints','num_food_est','num_food_poi','num_smoking']
	df_311 = pd.DataFrame(index=df.groupby('Incident Zip').mean().index)
	# start parsing
	for i in range(len(comp_types)):
		if comp_types[i]=='Total Complaints':
			df_311[cols[i]] = df.groupby('Incident Zip').count()['Unique Key'].values
		else:
			df_temp = df[df['Complaint Type']==comp_types[i]].groupby('Incident Zip').aggregate(len)['Unique Key'].reset_index().set_index('Incident Zip')
			df_311 = df_311.merge(df_temp, how='left', left_index=True, right_index=True, sort=True).rename(columns={'Unique Key':cols[i]})

	del df_311.index.name
	df_311.fillna(0, inplace=True)
	# finish parsing, write the dataframe to csv
	df_311.to_csv('../output/311_parsing_result.csv')