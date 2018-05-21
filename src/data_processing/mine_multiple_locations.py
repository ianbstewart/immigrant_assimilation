# -*- coding: utf-8 -*-
"""
Mine Facebook ads for multiple locations across a given query 
(e.g. all Hispanic ex-pats in LA, NYC).

@author: stewart
"""
from argparse import ArgumentParser
from src.data_processing.utils import query_facebook_audience
#import json
import os

LOC_DICT = {
        "3847" : "California",
        "3875" : "New York"
        }


def main():
    parser = ArgumentParser()
    parser.add_argument('--auth_file', default='data/facebook_auth.csv')
#    parser.add_argument('--query_file', default='data/ny_subregions.json')
    parser.add_argument('--query_file', default='data/hispanic_expats.json')
    parser.add_argument('--out_dir', default='data/query_results/')
#    parser.add_argument('--')
    args = parser.parse_args()
    auth_file = args.auth_file
    query_file = args.query_file
    out_dir = args.out_dir
#    location_list = args.location_list 
    query_base = os.path.basename(query_file).replace('.json', '')
    
    ## load data
    access_token, user_id = list(open(auth_file))[0].strip().split(',')
    
    ## issue query
    # make temp file
    results = query_facebook_audience(access_token, user_id, query_file)
    
    ## write to file
    out_file = os.path.join(out_dir, '%s.tsv'%(query_base))
    results.to_csv(out_file, sep='\t', index=False)
    
if __name__ == '__main__':
    main()