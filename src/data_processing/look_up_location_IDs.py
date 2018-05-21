# -*- coding: utf-8 -*-
"""
Mine IDs for arbitrary location queries on Facebook ads API.

@author: stewart
"""
from argparse import ArgumentParser
import os
import requests
from time import sleep
from src.data_processing.utils import load_facebook_auth
import pandas as pd
import json

MAX_ATTEMPTS=10

def query_location(query, access_token, loc_type=None, exact_matches=False):
    """
    query :: Location name to query.
    access_token :: FB API access token.
    loc_type :: Allowed location type (e.g. region).
    exact_matches :: Enforce exact name matching.
    """
    query_url = """https://graph.facebook.com/v2.11/search?access_token=%s&limit=10&locale=en_GB&method=get&q=%s&type=adgeolocation"""%(access_token, query)
    success = False
    attempt_ctr = 0
    while(not success and attempt_ctr < MAX_ATTEMPTS):
        try:
            query_result = requests.get(query_url)
            query_result_txt = query_result.text
            success = True
        ## sleep for rate-limiting
        except Exception, e:
            print('error with request = %s, going to sleep'%(e))
            sleep(1)
            attempt_ctr += 1
    result_data = json.loads(query_result_txt)
    data = result_data['data']
    if(loc_type is not None):
        data = list(filter(lambda x: x['type']==loc_type, data))
    ## restrict to exact matches
    if(exact_matches):
        data = list(filter(lambda x: x['name'].lower() == query.lower(), data))
    return data

def main():
    parser = ArgumentParser()
    parser.add_argument('--query_file', default='data/state_locs.txt')
    parser.add_argument('--out_dir', default='data/query_results/')
    parser.add_argument('--loc_type', default='region')
    args = parser.parse_args()
    query_file = args.query_file
    out_dir = args.out_dir
    loc_type = args.loc_type
    query_base = os.path.basename(query_file).replace('.txt', '')
    
    ## query for data
    access_token, user_id = load_facebook_auth()
    queries = list(map(lambda x: x.strip(), open(query_file)))
    print(queries)
    data_combined = []
    for query in queries:
        q_data = query_location(query, access_token, loc_type=loc_type, exact_matches=True)
        data_combined.append(pd.DataFrame(q_data))
    data_combined = pd.concat(data_combined, axis=0)
    print(data_combined.head())
    # restrict to relevant data
    relevant_cols = ['key', 'name', 'country_code']
    data_combined = data_combined.loc[:, relevant_cols]
    
    ## write to file
    out_file = os.path.join(out_dir, '%s.tsv'%(query_base))
    data_combined.to_csv(out_file, sep='\t', index=False)
    
if __name__ == '__main__':
    main()