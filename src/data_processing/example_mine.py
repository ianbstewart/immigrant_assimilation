from argparse import ArgumentParser
from pysocialwatcher import watcherAPI
import os
import requests
import json
import re

def query_facebook_audience(access_token, user_id, query):
    """
    Build manual query and execute request.
    """
    ## Lesvos ex-pats
#    query_url = ("""
#    https://graph.facebook.com/v2.11/act_%s/delivery_estimate?access_token=%s&optimization_goal=AD_RECALL_LIFT&targeting_spec={"age_max":65,"flexible_spec":[{"behaviors":[{"id":"6015559470583","name":"Ex-pats (All)"}]}],"geo_locations":{"custom_locations":[{"name":"(39.1382, 26.5054)","distance_unit":"kilometer","latitude":39.111615,"longitude":26.501907,"primary_city_id":871047,"radius":16,"region_id":4173,"country":"GR"}],"location_types":["home","recent"]},"facebook_positions":["feed"],"age_min":18,"device_platforms":["mobile","desktop"],"locales":[28],"publisher_platforms":["facebook"]}
#    """%(user_id, access_token)).strip()
     # replace lists with 0 element, long with int
    behavior_data = []
    for q_i in query['behavior']:
        q_fixed = {'id' : str(q_i['or'][0]).replace('L',''), 'name' : q_i['name']}
        behavior_data.append(q_fixed)
    behavior_str = ','.join(map(json.dumps, behavior_data))
    # fix quotes
    behavior_str = behavior_str.replace("'", '"')
#    int_fixer = re.compile("'(\d+)'")
#    behavior_str = int_fixer.sub(r'\1', behavior_str)
#    behavior_str = ','.join(map(lambda x: str({'id' : x['or'][0], 'name' : x['name']}), query['behavior']))
#    behavior_str = json.dumps({k.replace('or','id') : v for k,v in query['behavior'].items()})
    ## Lesvos ex-pats from specific countries
    ## TODO: fix location, age, gender
    
    query_url = ("""
    https://graph.facebook.com/v2.11/act_%s/delivery_estimate?access_token=%s&optimization_goal=AD_RECALL_LIFT&targeting_spec={"age_max":65,"flexible_spec":[{"behaviors":[%s]}],"geo_locations":{"custom_locations":[{"name":"(39.1382, 26.5054)","distance_unit":"kilometer","latitude":39.111615,"longitude":26.501907,"primary_city_id":871047,"radius":16,"region_id":4173,"country":"GR"}],"location_types":["home","recent"]},"facebook_positions":["feed"],"age_min":18,"device_platforms":["mobile","desktop"],"locales":[28],"publisher_platforms":["facebook"]}
    """%(user_id, access_token, behavior_str)).strip()
    print(query_url)
    try:
        response = requests.get(query_url)
    except Exception, e:
        print('could not execute query because error %s'%(e))
    
    return response
    #'https://graph.facebook.com/v2.11/act_10209683078339326/delivery_estimate?access_token=EAABsbCS1iHgBAL8E1ZAIJuDWJqZAS1XZBs6UxDkzB504YD23Xl3o06byXT6o2AhfwNL4LvdPt31gRzMLRQN5UT9T1mazVb3CrIWwXApZC1ga2UTatCMOaK0BIjQAfVkzGGU63MHPReJeqOP8BV1PkQwaWjgZBNEYz2T4G7WTTaWvNnDmZAUWuW&optimization_goal=AD_RECALL_LIFT&targeting_spec={%22age_max%22:65,%22flexible_spec%22:[{%22behaviors%22:[{%22id%22:%226015559470583%22,%22name%22:%22Ex-pats (All)%22}]}],%22geo_locations%22:{%22custom_locations%22:[{%22name%22:%22(39.1382, 26.5054)%22,%22distance_unit%22:%22kilometer%22,%22latitude%22:39.111615,%22longitude%22:26.501907,%22primary_city_id%22:871047,%22radius%22:16,%22region_id%22:4173,%22country%22:%22GR%22}],%22location_types%22:[%22home%22,%22recent%22]},%22facebook_positions%22:[%22feed%22],%22age_min%22:18,%22device_platforms%22:[%22mobile%22,%22desktop%22],%22locales%22:[28],%22publisher_platforms%22:[%22facebook%22]}'
    

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
#    output = watcher.run_data_collection(query_file)
    query_data = json.load(open(query_file))
    response = query_facebook_audience(access_token, user_id, query_data)
    print(response.text)
    
    ## write to file
#    if(not os.path.exists(out_dir)):
#        os.mkdir(out_dir)
#    out_base = os.path.basename(query_file).replace('.json', '.tsv')
#    out_file = os.path.join(out_dir, out_base)
#    output.to_csv(out_file, sep='\t')

if __name__ == '__main__':
	main()