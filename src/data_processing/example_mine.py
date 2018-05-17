from argparse import ArgumentParser
from pysocialwatcher import watcherAPI
import os
import re

#AGE_MIN=14
#AGE_MAX=70
#DEVICE_PLATFORMS = ['mobile', 'desktop']
#FACEBOOK_POSITIONS = ['feed']
def query_facebook_audience(access_token, user_id, query_file):
    """
    Build manual query and execute request.
    
    access_token :: FB access token
    user_id :: FB user ID
    query_file :: JSON file containing query
    
    response :: DataFrame with query response(s) => one response per row
    """
    watcher = watcherAPI()
    watcher.add_token_and_account_number(access_token, user_id)
    
    ## execute data collection
    response = watcher.run_data_collection(query_file)
    
    ## clean up temporary dataframes
    file_matcher = re.compile('dataframe_.*.csv')
    tmp_files = filter(lambda f: file_matcher.search(f) is not None, os.listdir('.'))
    for f in tmp_files:
        os.remove(f)
    
    ## old hard code
    ## Lesvos ex-pats
#    query_url = ("""
#    https://graph.facebook.com/v2.11/act_%s/delivery_estimate?access_token=%s&optimization_goal=AD_RECALL_LIFT&targeting_spec={"age_max":65,"flexible_spec":[{"behaviors":[{"id":"6015559470583","name":"Ex-pats (All)"}]}],"geo_locations":{"custom_locations":[{"name":"(39.1382, 26.5054)","distance_unit":"kilometer","latitude":39.111615,"longitude":26.501907,"primary_city_id":871047,"radius":16,"region_id":4173,"country":"GR"}],"location_types":["home","recent"]},"facebook_positions":["feed"],"age_min":18,"device_platforms":["mobile","desktop"],"locales":[28],"publisher_platforms":["facebook"]}
#    """%(user_id, access_token)).strip()
    ## old attempt to hard-code queries => bad idea!
#    query_fixed = {}
#     # replace lists with 0 element, long with int
#    behavior_data = []
#    for q_i in query['behavior']:
#        q_fixed = q_i.copy()
#        q_fixed['id'] = q_i['or'][0]
#        del(q_fixed['or'])
#        behavior_data.append(q_fixed)
#    query_fixed['flexible_spec'] = [{"behaviors" : behavior_data}]
#    query_fixed['age_min'] = AGE_MIN
#    query_fixed['age_max'] = AGE_MAX
#    if('ages_ranges' in query):
#        if('age_min' in query['ages_ranges'][0]):
#            query_fixed['age_min'] = query['age_ranges'][0]['min']
#        if('age_max' in query['ages_ranges'][0]):
#            query_fixed['age_max'] = query['age_ranges'][0]['max']
#    query_fixed['genders'] = query['genders']
#    query_fixed['facebook_positions'] = FACEBOOK_POSITIONS
#    query_fixed['device_platforms'] = DEVICE_PLATFORMS
    ## TODO: geolocation
    
    # update fixed query with remaining keys
    # clean up leftovers
#    query_fixed.update({k : query[k] for k in set(query.keys()) - set(query_fixed.keys())})
#    del(query_fixed['behavior'])
#    del(query_fixed['name'])
#    del(query_fixed['ages_ranges'])
#    query_fixed_str = json.dumps(query_fixed)
#    query_url = ("""                 
#                 https://graph.facebook.com/v2.11/act_%s/delivery_estimate?access_token=%s&optimization_goal=AD_RECALL_LIFT&targeting_spec=%s
#                 """%(user_id, access_token, query_fixed_str)).strip()
    
#    behavior_str = ','.join(map(json.dumps, behavior_data))
    # fix quotes
#    behavior_str = behavior_str.replace("'", '"')
#    int_fixer = re.compile("'(\d+)'")
#    behavior_str = int_fixer.sub(r'\1', behavior_str)
#    behavior_str = ','.join(map(lambda x: str({'id' : x['or'][0], 'name' : x['name']}), query['behavior']))
#    behavior_str = json.dumps({k.replace('or','id') : v for k,v in query['behavior'].items()})
    
#    query_url = ("""
#    https://graph.facebook.com/v2.11/act_%s/delivery_estimate?access_token=%s&optimization_goal=AD_RECALL_LIFT&targeting_spec={"age_max":65,"flexible_spec":[{"behaviors":[%s]}],"geo_locations":{"custom_locations":[{"name":"(39.1382, 26.5054)","distance_unit":"kilometer","latitude":39.111615,"longitude":26.501907,"primary_city_id":871047,"radius":16,"region_id":4173,"country":"GR"}],"location_types":["home","recent"]},"facebook_positions":["feed"],"age_min":18,"device_platforms":["mobile","desktop"],"locales":[28],"publisher_platforms":["facebook"]}
#    """%(user_id, access_token, behavior_str)).strip()
    
#    print('query URL:\n%s'%(query_url))
#    try:
#        response = requests.get(query_url)
#    except Exception, e:
#        print('could not execute query because error %s'%(e))
    
    return response

def main():
    parser = ArgumentParser()
    parser.add_argument('--auth_file', default='data/facebook_auth_ingmar.csv')
    parser.add_argument('--query_file', default='data/newyork_expats.json')
    parser.add_argument('--out_dir', default='data/')
    args = parser.parse_args()
    auth_file = args.auth_file
    query_file = args.query_file
    out_dir = args.out_dir    
    
    ## set up watcher
    watcher = watcherAPI()
    watcher.load_credentials_file(auth_file)
#    watcher.check_tokens_account_valid()
    access_token, user_id = list(open(auth_file))[0].strip().split(',')

    ## test query
    output = query_facebook_audience(access_token, user_id, query_file)
    
    ## write to file
    if(not os.path.exists(out_dir)):
        os.mkdir(out_dir)
    out_base = os.path.basename(query_file).replace('.json', '.tsv')
    out_file = os.path.join(out_dir, out_base)
    output.to_csv(out_file, sep='\t')

if __name__ == '__main__':
#    print(str(os.path.abspath('.')))
    main()