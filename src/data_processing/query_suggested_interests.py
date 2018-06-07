# -*- coding: utf-8 -*-
"""
Query FB ads API for suggested interests/behaviors/etc.

@author: stewart
"""
import requests
from argparse import ArgumentParser
import os
from src.data_processing.utils import load_facebook_auth
import pandas as pd

def mine_suggestions(suggestion_data, max_suggestions=2000):
    """
    Mine suggestions
    """
    

def main():
    parser = ArgumentParser()
    parser.add_argument('--suggestion_file', default='data/FB_suggestion_queries.csv')
    parser.add_argument('--max_suggestions', default=2000)
    args = parser.parse_args()
    suggestion_file = args.suggestion_file
    max_suggestions = args.max_suggestions
    
    ## load data
    suggestion_data = pd.read_csv(suggestion_file, sep=',', index_col=False)
    
    ## start mining
    suggestion_data_updated = mine_suggestions(suggestion_data, max_suggestions=max_suggestions)
    
if __name__ == '__main__':
    main()