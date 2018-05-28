# -*- coding: utf-8 -*-
"""
Mine Facebook for a given query's audience (daily and monthly).

@author: stewart
"""
from argparse import ArgumentParser
from src.data_processing.utils import query_and_write, load_facebook_auth
from pysocialwatcher import constants
import pandas as pd
import json
from ast import literal_eval

def main():
    parser = ArgumentParser()
#    parser.add_argument('--query_file', default='data/ny_subregions.json')
#    parser.add_argument('--query_file', default='data/hispanic_expat_lang_age.json')
#    parser.add_argument('--query_file', default='data/hispanic_lang_age.json')
#    parser.add_argument('--query_file', default='data/US_MX_native_interests.json')
#    parser.add_argument('--query_file', default='data/queries/US_MX_native_interests_top_3000_interest_new.json')
    parser.add_argument('--query_file', default='data/queries/hispanic_MX_expats_top_3000_interest.json')
    parser.add_argument('--interest_file', default='data/top_interests_complete_names.csv')
    parser.add_argument('--out_dir', default='data/query_results/')
    parser.add_argument('--response_file', default=None)
    args = parser.parse_args()
    query_file = args.query_file
    out_dir = args.out_dir
    response_file = args.response_file
    
    ## TEST: try multiple queries at once
    extra_auth_files = ['data/facebook_auth_ingmar.csv']
    
    ## temporary: remove interest IDs that we've already queried
#    response_file = 'dataframe_collecting_1527334686.csv'
#    responses = pd.read_csv(response_file, index_col=0).fillna(0, inplace=False)
#    responses_valid = responses[responses.loc[:, 'response'] != 0]
#    response_ids = list(set(responses_valid.loc[:, 'interests'].apply(lambda x: literal_eval(x)['or'][0])))
#    queries = json.load(open(query_file))
#    leftover_query = queries.copy()
#    leftover_query['interests'] = [i for i in leftover_query['interests'] if long(i['or'][0]) not in response_ids]
#    tmp_query_file = query_file.replace('.json', '_tmp.json')
#    print(tmp_query_file)
#    json.dump(leftover_query, open(tmp_query_file, 'w'), indent=4)
    
    query_and_write(query_file, out_dir, extra_auth_files=extra_auth_files, response_file=response_file)
    ## TODO: periodically copy response to server 
    ## so we can tell when something goes
    ## wrong even if we're not on the same machine
    ## easy implementation: cronjob
    
if __name__ == '__main__':
    main()