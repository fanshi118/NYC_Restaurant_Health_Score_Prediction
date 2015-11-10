# -*- coding: utf-8 -*-
"""
Yelp API v2.0 code sample.

This program demonstrates the capability of the Yelp API version 2.0
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/documentation for the API documentation.

This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
import numpy as np
import pandas as pd
import csv
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'NYC'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
#CONSUMER_KEY = 'MpAU-Y9CTlU0wZ8Hh4cL7Q'
#CONSUMER_SECRET = '5DDgjxYbL4sko3OgYsdTZHo4xvA'
#TOKEN = 'A3XLZ2RqoxyQBG8VdIQUV1yJjlCh7i34'
#TOKEN_SECRET = 'CVQZYNKKk2uZjrE57rzsp1cCrU0'
CONSUMER_KEY = YOUR_CONSUMER_KEY
CONSUMER_SECRET = YOUR_CONSUMER_SECRET
TOKEN = YOUR_TOKEN
TOKEN_SECRET = YOUR_TOKEN_SECRET

def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    #print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    #term = 'bars'

    df = pd.read_csv('data_result/DOHMH_ParsingResult.csv')
    df_zip = df['zip']
    zipList = df_zip.tolist()
    zipCodes = map(int, zipList)
    zipCodes = map(str, zipCodes)

    ratingDict = {}

    for zc in zipCodes:
        location = zc
        response = search(term, location)

        businesses = response.get('businesses')

        if not businesses:
            print u'No businesses for {0} in {1} found.'.format(term, location)
            return
            
        ratingList = []
        for i in range(len(businesses)):
            ratingList.append(businesses[i]['rating'])

        ratingDict[location] = np.mean(ratingList)

### Allocating the numerical values to different categories
### just to be consistent with the Yelp online rating if necessary
 #       tempMean = np.mean(ratingList)

 #       if (tempMean>=2.75) & (tempMean<3.25):
 #           ratingDict[zc] = 3.0
 #       if (tempMean>=3.25) & (tempMean<3.75):
 #           ratingDict[zc] = 3.5
 #       if (tempMean>=3.75) & (tempMean<4.25):
 #           ratingDict[zc] = 4.0
 #       if (tempMean>=4.25) & (tempMean<4.76):
 #           ratingDict[zc] = 4.5
 #       if (tempMean>=4.75):
 #           ratingDict[zc] = 5.0
 
    return ratingDict

    #print businesses[0].keys()

    '''
    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(
        len(businesses),
        business_id
    )

    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    pprint.pprint(response, indent=2)
    '''

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        result = query_api(input_values.term, input_values.location)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

    with open('data_result/NYC_YelpScore_Restaurants.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['zip', 'rest_score'])
        for key in sorted(result):
            writer.writerow([key,result[key]])

if __name__ == '__main__':
    main()
