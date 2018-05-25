# -*- coding: utf-8 -*-
"""
Mine Facebook for a given query's audience (daily and monthly).

@author: stewart
"""
from argparse import ArgumentParser
from src.data_processing.utils import query_and_write

def main():
    parser = ArgumentParser()
#    parser.add_argument('--query_file', default='data/ny_subregions.json')
#    parser.add_argument('--query_file', default='data/hispanic_expat_lang_age.json')
#    parser.add_argument('--query_file', default='data/hispanic_lang_age.json')
    parser.add_argument('--query_file', default='data/US_MX_native_interests.json')
    parser.add_argument('--out_dir', default='data/query_results/')
    args = parser.parse_args()
    query_file = args.query_file
    out_dir = args.out_dir
    
    query_and_write(query_file, out_dir)
    
if __name__ == '__main__':
    main()