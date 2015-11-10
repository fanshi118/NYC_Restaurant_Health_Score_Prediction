__author__ = 'Shi Fan'
import sys
import csv
import numpy as np
import pandas as pd

def read(file=None):
	_df = pd.read_csv(file)
	_df = _df[_df['ZIPCODE']>10000]
	_df = _df[~np.isnan(_df['ZIPCODE'])]
	return _df

def get_unique(_df=None):
	_unicodes = _df['ZIPCODE'].unique()
	_unicodes = _unicodes.astype(int)
	_unicodes.sort()
	_unids = _df['CAMIS'].unique()
	return _unicodes, _unids

def get_scores(_unids=None, _df_score=None):
	framesList = []
	print 'Start getting scores...will take a while. Go get some coffee...'
	for idn in _unids:
		_df_temp = _df_score.loc[_df_score.CAMIS==idn].drop_duplicates(subset='INSPECTION DATE')
		framesList.append(_df_temp)
	print 'Scores parsing complete!!!'
	_df_insp = pd.concat(framesList, ignore_index=True)
	return _df_insp

def data_parser(_unicodes=None, _df_cut=None, _df_vio=None, _df_insp=None):
	_df_DOHMH = pd.DataFrame(columns=['zip','num_restaurants','num_violations','num_Cviolations','avg_score'])
	row = 0
	print 'Start parsing data to our own data frame...'
	for zc in _unicodes:
		_df_DOHMH.loc[row,'zip'] = zc
		_df_DOHMH.loc[row,'num_restaurants'] = len(_df_cut[_df_cut['ZIPCODE']==zc])
		_df_DOHMH.loc[row,'num_violations'] = len(_df_vio[_df_vio['ZIPCODE']==zc])
		_df_DOHMH.loc[row,'num_Cviolations'] = len(_df_vio[(_df_vio['ZIPCODE']==zc)&(_df_vio['CRITICAL FLAG']=='Critical')])
		_df_DOHMH.loc[row,'avg_score'] = np.mean(_df_insp[_df_insp['ZIPCODE']==zc]['SCORE'])
		row += 1
	print 'Data parsing complete!!!'
	return _df_DOHMH

def main():
	''' dataset can be downloaded from here
		https://nycopendata.socrata.com/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/xx67-kt59
		click "Export" and "Download as CSV"
		save to folder named "data"
	'''
	# read in data and clean zip codes
	df = read('data/DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
	# get all the unique zip codes and CAMIS number (unique identifier)
	unicodes, unids = get_unique(df)
	
	# create three data frames for convenient parsing
	df_cut = df.drop_duplicates(subset='CAMIS') # to get the number of restaurants in each zip code
	df_vio = df.dropna(subset=['VIOLATION CODE']) # to get the number of violations in each zip code
	df_score = df.dropna(subset=['SCORE']) # to get the average score for restaurants in each zip code
	# go ahead get the average score in each zip code
	df_insp = get_scores(unids, df_score)

	# parse and summurize the dataset in our own data frame
	df_DOHMH = data_parser(_unicodes=unicodes, _df_cut=df_cut, _df_vio=df_vio, _df_insp=df_insp)
	# finish parsing, write the data frame to csv
	df_DOHMH.to_csv('data_result/DOHMH_ParsingResult.csv')

if __name__=='__main__':
	main()