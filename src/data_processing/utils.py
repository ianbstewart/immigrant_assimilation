# -*- coding: utf-8 -*-
"""
Utilities for data collection and analysis.

@author: stewart
"""
import os
import re
from pysocialwatcher import watcherAPI

def query_facebook_audience(access_token, user_id, query_file):
    """
    Build manual query and execute request.
    
    access_token :: FB access token
    user_id :: FB user ID
    query_file :: JSON file containing query
    
    response :: DataFrame with query response(s) => one response per row
    """
    watcher = watcherAPI()
    watcher.add_token_and_account_number(access_token, user_id)
    
    ## execute data collection
    response = watcher.run_data_collection(query_file)
    
    ## clean up temporary dataframes
    file_matcher = re.compile('dataframe_.*.csv')
    tmp_files = filter(lambda f: file_matcher.search(f) is not None, os.listdir('.'))
    for f in tmp_files:
        os.remove(f)
    
    return response

def load_facebook_auth(auth_file='data/facebook_auth.csv'):
    """
    Load Facebook ad API authentication from file.
    
    auth_file :: File name.
    
    access_token :: Access token.
    user_id :: User ID.
    """
    access_token, user_id = list(open(auth_file))[0].strip().split(',')
    return access_token, user_id