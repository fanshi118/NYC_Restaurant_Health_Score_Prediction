__author__ = 'Shi Fan'
import sys
import csv
import pandas as pd
import numpy as np

if __name__=='__main__':
	# dataset can be downloaded from here
	# https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
	# set filter: "Agency is DOHMH" and "Location Type contains Restaurant"
	# click "Export" and "Download as CSV"
	df = pd.read_csv('data/311_DOHMH_Restaurant.csv')
	# cleaning data
	df = df[df['Incident Zip']!='NY']
	df['Incident Zip'] = df['Incident Zip'].astype(float)
	df = df.dropna(subset=['Incident Zip'])
	df['Incident Zip'] = df['Incident Zip'].astype(int)
	df = df[(df['Incident Zip']>10000) & (df['Incident Zip']<20000)]
	# get unique zip codes
	unicodes = df['Incident Zip'].unique()
	unicodes = unicodes.astype(int)
	unicodes.sort()
	# initialize a dataframe to store data
	df_311 = pd.DataFrame(columns=['zip','num_complaints','num_food_est','num_food_poi','num_smoking'])
	# start parsing
	row = 0
	for zc in unicodes:
		df_311.loc[row,'zip'] = zc
		df_311.loc[row,'num_complaints'] = len(df[df['Incident Zip']==zc])
		df_311.loc[row,'num_food_est'] = len(df[(df['Incident Zip']==zc) & (df['Complaint Type']=='Food Establishment')])
		df_311.loc[row,'num_food_poi'] = len(df[(df['Incident Zip']==zc) & (df['Complaint Type']=='Food Poisoning')])
		df_311.loc[row,'num_smoking'] = len(df[(df['Incident Zip']==zc) & (df['Complaint Type']=='Smoking')])
		row += 1
	# finish parsing, write the dataframe to csv
	df_311.to_csv('data_result/311_ParsingResult.csv')