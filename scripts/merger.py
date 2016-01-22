__author__ = 'Shi Fan'
import sys
import csv
import numpy as np
import pandas as pd

if __name__=='__main__':

	# merge 311 with DOHMH inspection
	df_311 = pd.read_csv('../output/311_parsing_result.csv')
	df_DOHMH = pd.read_csv('../output/dohmh_parsing_result.csv')
	df_merge = pd.merge(df_311, df_DOHMH, how='right', left_index=True, right_index=True, sort=True).drop(['Unnamed: 0_x'], axis=1).rename(columns={'Unnamed: 0_y': 'zipcode'}).fillna(0)

	# merge yelp bar scores with restaurant scores
	df_yelp_bar = pd.read_csv('../output/yelp_bars_scraped.csv').rename(columns={'rating':'bar_rating','review_count':'bar_rev_count'})
	df_yelp_rest = pd.read_csv('../output/yelp_restaurants_scraped.csv').rename(columns={'rating':'rest_rating','review_count':'rest_rev_count'})
	df_yelp = pd.merge(df_yelp_bar, df_yelp_rest, left_index=True, right_index=True, sort=True).drop(['Unnamed: 0_y'], axis=1).rename(columns={'Unnamed: 0_x': 'zipcode'})

	# merge the two merged datasets together
	df_final = pd.merge(df_yelp, df_merge, on='zipcode', sort=True).set_index('zipcode')
	del df_final.index.name
	df_final.to_csv('../output/merged.csv')