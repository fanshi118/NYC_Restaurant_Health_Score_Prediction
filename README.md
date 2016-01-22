# Restaurant Health Quality Prediction Project

## Overview
This project demonstrates the capability to predict the overall health score 
of restaurants in each zip code of New York City by using 311 complaints data, 
DOHMH inspection data, and social media data from Yelp API. 

## Steps to run

To install the dependencies, run:
`pip install yelpapi`.

Download the datasets specified in the `input` folder.

Run the code to parse 311 and DOHMH inspection data:
`python 311_parser.py`
`python DOHMH_parser.py`

Run the code to get the average scores and review counts of restaurants and bars 
using Yelp API:
`python yelp_parser.py restaurants`
`python yelp_parser.py bars`

Run the code to merge all parsed data from different sources together:
`python merger.py`

To see the regression result on the merged dataset `merged.csv`:
    PCA --> run the notebook `analysis_PCA.ipynb`,
    Lasso --> run the notebook `analysis_Lasso.ipynb`,
    Random Forest --> run the notebook `analysis_RandomForest.ipynb`

All parsed datasets, plus a json file specifying the weights for the Lasso model 
are in the `output` folder.
All plots and maps are in the `figures` folder.
