__author__ = 'Shi Fan'
import sys
import csv
import numpy as np
import pandas as pd

if __name__=='__main__':

	# merge 311 with DOHMH inspection
	df_311 = pd.read_csv('data_result/311_ParsingResult.csv')
	df_DOHMH = pd.read_csv('data_result/DOHMH_ParsingResult.csv')
	df_311.reset_index()
	df_DOHMH.reset_index()
	df_merge = pd.merge(df_311, df_DOHMH, how='outer', on='zip', sort=True)
	df_merge.drop(['Unnamed: 0_x','Unnamed: 0_y'], axis=1, inplace=True)
	df = df_merge.dropna(subset=['num_restaurants'])
	df['num_complaints'] = df['num_complaints'].fillna(0)

	# merge yelp bar scores with restaurant scores
	df_yelp_bar = pd.read_csv('data_result/NYC_YelpScore_Bars.csv')
	df_yelp_rest = pd.read_csv('data_result/NYC_YelpScore_Restaurants.csv')
	df_yelp = pd.merge(df_yelp_bar, df_yelp_rest, on='zip', sort=True)

	# merge the two merged datasets together
	df_final = pd.merge(df_yelp, df, on='zip', sort=True)
	df_final.to_csv('data_result/Merged.csv')