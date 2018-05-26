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
#    parser.add_argument('--interest_count_file', default='data/all_FB_interests_2016/all_FB_interests_2016.csv')
    parser.add_argument('--interest_sorted_file', default='data/top_interests_complete.json')
    parser.add_argument('--query_file', default='data/queries/US_MX_native_interests.json')
    parser.add_argument('--top_k', default=3000)
    args = parser.parse_args()
#    interest_count_file = args.interest_count_file
    interest_sorted_file = args.interest_sorted_file
    query_file = args.query_file
    top_k = args.top_k
    
    ## load data
#    interest_counts = pd.read_csv(interest_count_file, sep=',', index_col=False)
#    interest_counts.loc[:, 'id'] = interest_counts.loc[:, 'id'].fillna(0, inplace=False)
#    interest_counts.loc[:, 'id'] = interest_counts.loc[:, 'id'].astype(long)
    interest_data = json.load(open(interest_sorted_file))['data']
    interests = pd.DataFrame(interest_data)
    query = json.load(open(query_file))
    
    ## cut off at top-k
#    interest_counts.sort_values('audience_size', inplace=True, ascending=False)
    interests_k = interests.head(n=top_k)
    
    ## update query
    interests_k = interests_k.loc[:, ['id', 'name']]
    query['interests'] = [{'name' : [r.loc['name']], 'or' : [r.loc['id']]} for _, r in interests_k.iterrows()]
    
    ## write
    out_file = query_file.replace('.json', '_top_%d_interest.json'%(top_k))
    print(out_file)
    json.dump(query, open(out_file, 'w'), indent=4, encoding='latin1')
    
if __name__ == '__main__':
    main()