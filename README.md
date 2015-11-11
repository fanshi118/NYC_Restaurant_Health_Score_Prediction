# Restaurant Health Quality Prediction Project

## Overview
This project demonstrates the capability to predict the overall health score 
of restaurants in each zip code of New York City by using 311 complaints data, 
DOHMH inspection data, and social media data from Yelp API. 

## Steps to run

To install the dependencies, run:
`pip install -r requirements.txt`.

Download the datasets specified in `311_parser.py` and `DOHMH_parser.py` and put 
them in a folder called "data"

Run the code to parse 311 and DOHMH inspection data:
`python 311_parser.py`
`python DOHMH_parser.py`

Run the code to get the average scores of restaurants and bars using Yelp API:
`python yelp_get_avg.py`

Run the code to merge all parsed data from different sources together:
`python merger.py`

Run the ipython notebook `analysis.ipynb` to see the result of regression 
analysis on the merged dataset `Merged.csv`

All parsed datasets are in the "data_result" folder.
All graphs and plots are in the "imgs" folder.
