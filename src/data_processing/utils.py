# -*- coding: utf-8 -*-
"""
Utilities for data collection and analysis.

@author: stewart
"""
import os
import re
from pysocialwatcher import watcherAPI
from pysocialwatcher.constants import TOKENS
import json

def query_facebook_audience(access_token, user_id, query_file, extra_auth_data=[], response_file=None):
    """
    Build manual query and execute request.
    
    access_token :: FB access token
    user_id :: FB user ID
    query_file :: JSON file containing query
    extra_auth_data :: List of auth data pairs.
    response_file :: Name of existing response file, if needed.
    
    response :: DataFrame with query response(s) => one response per row
    """
    watcher = watcherAPI()
    if(not (access_token, user_id) in TOKENS):
        watcher.add_token_and_account_number(access_token, user_id)
    for (access_token_i, user_id_i) in extra_auth_data:
        if(not (access_token_i, user_id_i) in TOKENS):
            watcher.add_token_and_account_number(access_token_i, user_id_i)
    print('%d FB tokens'%(len(TOKENS)))
    
    ## execute data collection
    if(response_file is not None and os.path.exists(response_file)):
        print('using response file %s'%(response_file))
        response = watcher.load_data_and_continue_collection(response_file)
    else:
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
    app_id :: App ID.
    app_secret :: Secret app ID.
    """
    auth_data = list(open(auth_file))[0].strip().split(',')
    if(len(auth_data) == 2):
        access_token, user_id = auth_data
        app_id = None
        app_secret = None
    elif(len(auth_data) == 4):
        access_token, user_id, app_id, app_secret = auth_data
#    access_token, user_id = list(open(auth_file))[0].strip().split(',')[:2]
    return access_token, user_id, app_id, app_secret

def query_and_write(query_file, out_dir, extra_auth_files=[], response_file=None):
    """
    Query Facebook for specified JSON target and
    write results to out_dir as .tsv.
    
    query_file :: JSON file containing query
    out_dir :: Output directory.
    extra_auth_files :: Extra FB auth data files.
    response_file :: Name of existing response file, if needed.
    """
    access_token, user_id, _, _ = load_facebook_auth()
    query_base = os.path.basename(query_file).replace('.json', '')
    
    ## issue query
    extra_auth_data = [load_facebook_auth(auth_file=f)[:2] for f in extra_auth_files]
    results = query_facebook_audience(access_token, user_id, query_file, extra_auth_data=extra_auth_data, response_file=response_file)
    
    ## clean up JSON cols
    json_cols = filter(lambda x: type(results.loc[:, x].iloc[0]) is dict, results.columns)
    for c in json_cols:
        results.loc[:, c] = results.loc[:, c].apply(json.dumps)
    
    ## write to file
    out_file = os.path.join(out_dir, '%s.tsv'%(query_base))
    results.to_csv(out_file, sep='\t', index=False)