# -*- coding: utf-8 -*-
"""
Remove invalid interests from top interests.
Assume that we have already queried FB for interests
in check_interest_id_valid.py.

@author: stewart
"""
from argparse import ArgumentParser
import pandas as pd
import json

def main():
    parser = ArgumentParser()
    parser.add_argument('--interest_file', default='data/top_interests_complete.json')
    parser.add_argument('--interest_name_file', default='data/top_interests_complete_names.csv')
    args = parser.parse_args()
    interest_file = args.interest_file
    interest_name_file = args.interest_name_file
    
    ## load data
    interest_data = json.load(open(interest_file))
    interest_name_data = pd.read_csv(interest_name_file, index_col=False, na_filter=False)
    
    ## remove from interest data
    ## all interests without valid name
    invalid_name_data = interest_name_data[interest_name_data.loc[:, 'interest_name'] == 'NA']
    invalid_ids = invalid_name_data.loc[:, 'interest_id'].values
    total_interests = len(interest_data['data'])
    interest_data['data'] = filter(lambda x: long(x['id']) not in invalid_ids, interest_data['data'])
    print('%d/%d clean interests'%(len(interest_data['data']), total_interests))

    ## write to file
    out_file = interest_file.replace('.json', '_clean.json')
    json.dump(interest_data, open(out_file, 'w'), indent=4)

if __name__ == '__main__':
    main()