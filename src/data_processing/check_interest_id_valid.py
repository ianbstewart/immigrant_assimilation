# -*- coding: utf-8 -*-
"""
Query Facebook for top interest IDs to determine if/how they have changed.

@author: stewart
"""
import json
from argparse import ArgumentParser
from src.data_processing.utils import load_facebook_auth
import requests
from time import sleep
import pandas as pd
import logging
import os
import math

## suppress request INFO messages
logging.getLogger("requests").setLevel(logging.WARNING)

MAX_QUERIES=10
SLEEP_TIME=1
RATE_LIMIT_SLEEP_TIME=300
def interest_name_query(access_token, user_id, interest_id):
    """
    Query FB for name of interest given the ID.
    
    access_token :: FB access token
    user_id :: FB user ID
    interest_id :: interest ID number
    
    interest_name :: name of interest
    """
    header_url = 'https://graph.facebook.com/v2.11/act_%s/targetingsentencelines'%(user_id)
    targeting_spec={
            "geo_locations" :
                {
                        "countries":["US"],
                        "location_types":["home"]
                },
            "flexible_spec":
                [
                        {
                                "interests":
                                    [
                                            {
                                                    "id" : interest_id
                                            }
                                    ]
                        }
                ]
                  }
    params = {
            'access_token' : access_token,
            'optimize_for' : 'NONE',
            'targeting_spec' : json.dumps(targeting_spec)
            }
    full_header_url = 'https://graph.facebook.com/v2.11/act_%s/targetingsentencelines?access_token=%s&_reqName=adaccount/targetingsentencelines&method=get&targeting_spec={"geo_locations":{"countries":["US"],"location_types":["home"]},"flexible_spec":[{"interests":[{"id":"%s"}]}],"targeting_optimization":"none"}'%(user_id, access_token, interest_id)
    success = False
    query_ctr = 0
    interest_name = ''
    while(not success and query_ctr < MAX_QUERIES):
        try:
            # the official way to call the API
#            response = requests.get(header_url, params=params)
            # the hacky way to call the API (might get around rate limits)
            response = requests.get(full_header_url)
            response_json = json.loads(response.text)
            if('error' in response_json):
                error_code = response_json['error']['code']
                ## rate limit error
                if(error_code == 17):
                    print('rate limit reached at id=%d, sleeping for %d seconds'%(interest_id, RATE_LIMIT_SLEEP_TIME))
                    sleep(RATE_LIMIT_SLEEP_TIME)
                    success = True
            else:
                response_data = response_json['targetingsentencelines']
                if(len(response_data) > 3):
                    interest_data = response_data[3]['children']
                    interest_name = interest_data[0]
                    interest_name = interest_name.replace('Interests: ', '')
                success = True
                sleep(SLEEP_TIME*.25)
        except Exception, e:

            print(response_json)
            print('bad params:%s'%(json.dumps(params, indent=4)))
            print(e)
            query_ctr += 1
            sleep(SLEEP_TIME)
    return interest_name

def interest_name_query_batch(access_token, user_id, interest_ids):
    """
    Query batch of interest IDs for more efficient access.
    
    access_token :: FB access token
    user_id :: FB user ID
    interest_ids :: FB interest IDs
    
    interest_names :: FB interest names
    """
    targeting_spec={
            "geo_locations" :
                {
                        "countries":["US"],
                        "location_types":["home"]
                },
            "flexible_spec":
                [
                        {
                                "interests":
                                    [
                                            {
                                                    "id" : interest_id
                                            }
                                    ]
                        }
                        for interest_id in interest_ids
                ]
                  }
    params = {
            'access_token' : access_token,
            'optimize_for' : 'NONE',
            'targeting_spec' : json.dumps(targeting_spec)
            }
    header_url = 'https://graph.facebook.com/v2.11/act_%s/targetingsentencelines'%(user_id)
    success = False
    query_ctr = 0
    interest_names = []
    while(not success and query_ctr < MAX_QUERIES):
        try:
            # the official way to call the API
            response = requests.get(header_url, params=params)
            response_json = json.loads(response.text)
            if('error' in response_json):
                error_code = response_json['error']['code']
                ## rate limit error
                if(error_code == 17):
                    print('rate limit reached at id=%d, sleeping for %d seconds'%(interest_id, RATE_LIMIT_SLEEP_TIME))
                    sleep(RATE_LIMIT_SLEEP_TIME)
                    success = True
            else:
                response_data = response_json['targetingsentencelines']
                response_data_matches = filter(lambda x: x['content']=='People Who Match:' or x['content']=='And Must Also Match:', 
                                               response_data)
                interest_names = [m['children'][0].replace('Interests: ','') 
                                  for m in response_data_matches]
                success = True
                sleep(SLEEP_TIME*.25)
        except Exception, e:
            print(response_json)
            print('bad params:%s'%(json.dumps(params, indent=4)))
            print(e)
            query_ctr += 1
            sleep(SLEEP_TIME)
    return interest_names

def query_test():
    """
    Unit test for interest ID queries.
    """
    access_token, user_id = load_facebook_auth('data/facebook_auth_ingmar.csv')
    interest_id_1 = 6003221234467 # Mexico City
    interest_name_1 = interest_name_query(access_token, user_id, interest_id_1)
    print(interest_name_1)
    assert interest_name_1 == 'Mexico City'
    interest_id_2 = 6002964065372 # Lewis and Clark-class dry cargo ship => ID doesn't work
    interest_name_2 = interest_name_query(access_token, user_id, interest_id_2)
    print(interest_name_2)
    assert interest_name_2 == 'Off' or interest_name_2 == ''
    print('query test success')

def main():
    parser = ArgumentParser()
    parser.add_argument('--interest_file', default='data/top_interests_complete.json')
    args = parser.parse_args()
    interest_file = args.interest_file
    interest_ids, interest_names = zip(*[(long(i['id']), i['name']) 
                                         for i in json.load(open(interest_file))['data']])
    access_token, user_id = load_facebook_auth()
#    interest_ids = interest_ids[:10]
#    query_test()
    
    ## old approach: collect names for all IDs
    ## collect name data
#    interest_data = pd.DataFrame()
#    out_file = interest_file.replace('.json', '_names.csv')
#    if(os.path.exists(out_file)):
#        interest_data = pd.read_csv(out_file, sep=',', index_col=False)
#        interest_ids = filter(lambda x: x not in interest_data.loc[:, 'interest_id'].values, interest_ids)
#    write_out_count = 10
#    for i, interest_id in enumerate(interest_ids):
#        interest_name = interest_name_query(access_token, user_id, interest_id)
#        interest_data = interest_data.append([[interest_id, interest_name]])
#        if(interest_data.shape[0] == 1):
#            interest_data.columns = ['interest_name', 'interest_id']
#        if(i % write_out_count == 0):
#            interest_data.to_csv(out_file, sep=',', index=False, encoding='utf-8')
#        if(i % 100 == 0):
#            print('processed %d interests'%(i))
    
    ## new approach: collect all ids and names but
    ## mark the invalid ones based on whether 
    ## their names are missing from results
    batch_size = 25
#    cutoff = 75
#    interest_ids = interest_ids[:cutoff]
#    interest_names = interest_names[:cutoff]
    interest_data = pd.DataFrame()
    out_file = interest_file.replace('.json', '_names.csv')
    if(os.path.exists(out_file)):
        interest_data = pd.read_csv(out_file, sep=',', index_col=False)
        interest_id_names = zip(interest_ids, interest_names)
        interest_ids, interest_names = zip(*filter(lambda x: x[0] not in interest_data.loc[:, 'interest_id'].values, interest_id_names))
    interest_data_cols = ['interest_id', 'interest_name']
    batches = int(math.ceil(len(interest_ids) / batch_size))
    write_ctr = 5
    for i in range(batches):
        interest_ids_i = interest_ids[i*batch_size:(i+1)*batch_size]
        interest_names_i = interest_names[i*batch_size:(i+1)*batch_size]
        response_names_i = interest_name_query_batch(access_token, user_id, interest_ids_i)
        fixed_names_i = ['NA' if x not in set(interest_names_i) else x for x in response_names_i]
        interest_data_i = pd.DataFrame([interest_ids_i, fixed_names_i], index=interest_data_cols).transpose()
        interest_data = interest_data.append(interest_data_i)
        if(i % write_ctr == 0):
            interest_data.to_csv(out_file, sep=',', index=False, encoding='utf-8')
        if(i % 10 == 0):
            print('processed %d interests'%(batch_size*(i+1)))
    
    ## write to file
    interest_data.to_csv(out_file, sep=',', index=False, encoding='utf-8')
    
if __name__ == '__main__':
    main()