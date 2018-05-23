# -*- coding: utf-8 -*-
"""
Mine Facebook ads for multiple locations across a given query 
(e.g. all Hispanic ex-pats in LA, NYC).

@author: stewart
"""
from argparse import ArgumentParser
from src.data_processing.utils import query_facebook_audience
import json
import os

def main():
    parser = ArgumentParser()
    parser.add_argument('--auth_file', default='data/facebook_auth.csv')
#    parser.add_argument('--query_file', default='data/ny_subregions.json')
#    parser.add_argument('--query_file', default='data/hispanic_expat_lang_age.json')
    parser.add_argument('--query_file', default='data/hispanic_lang_age.json')
    parser.add_argument('--out_dir', default='data/query_results/')
    args = parser.parse_args()
    auth_file = args.auth_file
    query_file = args.query_file
    out_dir = args.out_dir
#    location_list = args.location_list 
    query_base = os.path.basename(query_file).replace('.json', '')
    
    ## load data
    access_token, user_id = list(open(auth_file))[0].strip().split(',')
    
    ## issue query
    results = query_facebook_audience(access_token, user_id, query_file)
    
    ## clean up JSON cols
    json_cols = filter(lambda x: type(results.loc[:, x].iloc[0]) is dict, results.columns)
    for c in json_cols:
        results.loc[:, c] = results.loc[:, c].apply(json.dumps)
    
    ## write to file
    out_file = os.path.join(out_dir, '%s.tsv'%(query_base))
    results.to_csv(out_file, sep='\t', index=False)
    
if __name__ == '__main__':
    main()