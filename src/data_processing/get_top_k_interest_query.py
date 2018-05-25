# -*- coding: utf-8 -*-
"""
Build FB ad query based on top-k interests.

@author: stewart
"""
import json
from argparse import ArgumentParser
import pandas as pd

def main():
    parser = ArgumentParser()
    parser.add_argument('--interest_count_file', default='data/all_FB_interests_2016/all_FB_interests_2016.csv')
    parser.add_argument('--query_file', default='data/US_MX_native_interests.json')
    parser.add_argument('--top_k', default=3000)
    args = parser.parse_args()
    interest_count_file = args.interest_count_file
    query_file = args.query_file
    top_k = args.top_k
    
    ## load data
    interest_counts = pd.read_csv(interest_count_file, sep=',', index_col=False)
    query = json.load(open(query_file))
    
    ## cut off at top-k
    interest_counts.sort_values('audience_size', inplace=True, ascending=False)
    interest_counts_k = interest_counts.head(n=top_k)
    
    ## update query
    interests_k = interest_counts.loc[:, ['id', 'name']]
    query['interests'] = [r.to_dict() for _, r in interests_k.iterrows()]
    print(query)
    
    ## write
    
    
if __name__ == '__main__':
    main()