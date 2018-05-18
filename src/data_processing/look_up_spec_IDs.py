from argparse import ArgumentParser
import os
import pandas as pd
import requests
import json

def query_spec_data(spec_name, user_ID, access_token):
    """
    Query FB for data corresponding to spec_name.
    
    spec_name :: name of specification (e.g. "Brazil" => "Brazil (Ex-pats)")
    user_ID :: FB user ID
    access_token :: FB access token
    
    spec_data :: spec data (ID, full name, audience, etc.)
    """
    query_URL = 'https://graph.facebook.com/v2.11/act_%s/targetingsearch?access_token=%s&q=%s'%(user_ID, access_token, spec_name)
    response = None
    while(response is None):
        try:
            response = requests.get(query_URL)
            ## TODO: handle error codes
#            if(response.code)
        except Exception, e:
            print('query error\n%s'%(e))
            response = 'NULL'
    # extract names and IDs from response
    spec_data = pd.DataFrame()
    if(response != 'NULL'):
        response_data = json.loads(response.text)
        if(response_data.get('data') is not None):
            spec_data_response = response_data['data']
            spec_data = pd.DataFrame(spec_data_response)
    
    ## add query name for bookkeeping
    spec_data.loc[:, 'query'] = spec_name
    return spec_data

def main():
    parser = ArgumentParser()
    parser.add_argument('--auth_file', default='data/facebook_auth_ingmar.csv')
    parser.add_argument('--spec_name_file', default='data/spec_names.txt')
    parser.add_argument('--spec_data_file', default='data/spec_data.tsv')
    args = parser.parse_args()
    auth_file = args.auth_file
    spec_name_file = args.spec_name_file
    spec_data_file = args.spec_data_file
    
    ## load data
    access_token, user_ID = list(open(auth_file))[0].strip().split(',')
    spec_names = [l.strip() for l in open(spec_name_file)]
    # if spec IDs exist, load from file so we don't double-dip
    if(os.path.exists(spec_data_file)):
        spec_datas = pd.read_csv(spec_data_file, sep='\t')
        # only query names that have already been queried
        spec_names = list(set(spec_names) - set(spec_datas.loc[:, 'query'].unique()))
    else:
        spec_datas = pd.DataFrame()
        
    ## query
    for spec_name in spec_names:
        spec_data = query_spec_data(spec_name, user_ID, access_token)
        spec_datas = spec_datas.append(spec_data)
#        print(spec_datas)
    
    ## deduplicate
    spec_datas.drop_duplicates(['id', 'name'], keep='last', inplace=True)
    
    ## write to file
    spec_datas.to_csv(spec_data_file, sep='\t', index=False)
    
if __name__ == '__main__':
#    print(str(os.path.abspath('.')))
    main()