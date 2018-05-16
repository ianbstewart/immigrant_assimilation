from argparse import ArgumentParser
from pysocialwatcher import watcherAPI
import os

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
    watcher.check_tokens_account_valid()

    ## test query
    output = watcher.run_data_collection(query_file)
    
    ## write to file
    if(not os.path.exists(out_dir)):
        os.mkdir(out_dir)
    out_base = os.path.basename(query_file).replace('.json', '.tsv')
    out_file = os.path.join(out_dir, out_base)
    output.to_csv(out_file, sep='\t')

if __name__ == '__main__':
	main()