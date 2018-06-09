# -*- coding: utf-8 -*-
"""
Query FB ads API for suggested interests/behaviors/etc.

@author: stewart
"""
from argparse import ArgumentParser
import os
from src.data_processing.utils import load_facebook_auth
import pandas as pd
from facebookads.adobjects.targetingsearch import TargetingSearch
from facebookads.session import FacebookSession
from facebookads.api import FacebookAdsApi
import codecs

def mine_suggestions(suggestion_data, max_suggestions=2000):
    """
    Mine suggestions for all interests provided, add suggestions
    to queue, keep mining until we hit the max.
    
    :param suggestion_data: list of suggested interest names
    :param max_suggestions: max number of suggestions to mine
    :return:: new_suggestion_data: Name, ID info for all new suggestions.
    """
    access_token, user_id, app_id, app_secret = load_facebook_auth()
    session = FacebookSession(app_id, app_secret, access_token)
    api = FacebookAdsApi(session)
    new_suggestion_data = pd.DataFrame()
    suggestion_queue = []
    suggestion_queue += suggestion_data
    suggestions_per_query = 1
    relevant_cols = ['id', 'name', 'topic', 'path', 'audience']
    while(new_suggestion_data.shape[0] < max_suggestions and 
          len(suggestion_queue) > 0):
        s = suggestion_queue[:suggestions_per_query]
        print('total data=%d; processing suggestions %s'%
              (new_suggestion_data.shape[0], ','.join(s)))
        suggestion_queue = suggestion_queue[suggestions_per_query:]
        params = {
                'type' : 'adinterestsuggestion',
                'interest_list' : s,
                }
        s_results = TargetingSearch.search(params=params, api=api)
        s_df = pd.DataFrame(s_results)
        s_df = s_df.loc[:, set(relevant_cols) & set(s_df.columns)]
        # temp: restrict to top-k results to stay on-topic
        s_df = s_df.iloc[:25, :]
        # remove duplicates
        if(s_df.shape[0] > 0):
            if(new_suggestion_data.shape[0] > 0):
                s_df = s_df[~s_df.loc[:, 'id'].isin(new_suggestion_data.loc[:, 'id'])]
            new_suggestion_data = new_suggestion_data.append(s_df)
            # add new names to suggestion data
            suggestion_queue += s_df.loc[:, 'name'].values.tolist()
    return new_suggestion_data

def main():
    parser = ArgumentParser()
#    parser.add_argument('--suggestion_file', default='data/FB_suggestion_interests.csv')
    parser.add_argument('--suggestion_file', default='data/query_results/top_latin_american_music.txt')
    parser.add_argument('--max_suggestions', default=2000)
    args = parser.parse_args()
    suggestion_file = args.suggestion_file
    max_suggestions = args.max_suggestions
    
    ## load data
    if('.csv' in suggestion_file):
        suggestion_data = pd.read_csv(suggestion_file, sep=',', index_col=False)
        suggestion_names = suggestion_data.loc[:, 'name'].values.tolist()
    elif('.txt' in suggestion_file):
        suggestion_names = [l.strip() for l in codecs.open(suggestion_file)]
    
    ## start mining
    suggestion_data_updated = mine_suggestions(suggestion_names, max_suggestions=max_suggestions)
    
    ## write to file
    out_file = suggestion_file.replace(os.path.splitext(suggestion_file)[1], 
                                       '_suggestion_results.tsv')
#    print(out_file)
    suggestion_data_updated.to_csv(out_file, sep='\t', index=False, encoding='utf-8')
    
if __name__ == '__main__':
    main()