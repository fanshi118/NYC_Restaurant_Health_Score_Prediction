__author__='Shi Fan'
import sys
import pandas as pd
from yelpapi import YelpAPI

consumer_key = 'MpAU-Y9CTlU0wZ8Hh4cL7Q'
consumer_secret = '5DDgjxYbL4sko3OgYsdTZHo4xvA'
token = 'A3XLZ2RqoxyQBG8VdIQUV1yJjlCh7i34'
token_secret = 'CVQZYNKKk2uZjrE57rzsp1cCrU0'

def get_zips(myfile=None):
	zips = pd.read_csv(myfile, index_col=0).index
	zipList = zips.tolist()
	zipCodes = map(int, zipList)
	zipCodes = map(str, zipCodes)
	return zipCodes

def get_ratings_and_reviews(_d=None,zipCodes=None,yelp_api=None):
	for i in zipCodes:
		_d['rating'].setdefault(i,0)
		_d['review_count'].setdefault(i,0)

		print 'Querying businesses for %s...' % i
		search_results = yelp_api.search_query(term=sys.argv[1],location=i)
		businesses = search_results.get('businesses')

		count = 0
		rating = 0
		review = 0
		for biz in businesses:
			if biz['location']['display_address'][-1][-5:]==i:
				rating += biz['rating']
				review += biz['review_count']
				count += 1

		if count==0:
			_d['rating'][i] = 0
			_d['review_count'][i] = 0
		else:
			_d['rating'][i] = rating/count
			_d['review_count'][i] = review/count

	return _d

def main():
	yelp_api = YelpAPI(consumer_key, consumer_secret, token, token_secret)
	features = ['rating', 'review_count']
	d = {}
	for f in features:
		d.setdefault(f,{})

	zips = get_zips('../output/dohmh_parsing_result.csv')
	d_ = get_ratings_and_reviews(d,zips,yelp_api)

	df = pd.DataFrame(data=d, index=zips, columns=features)
	df.to_csv('../output/yelp_%s_scraped.csv' % sys.argv[1])

if __name__=='__main__':
	main()