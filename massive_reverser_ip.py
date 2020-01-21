#!/usr/bin/env python3
# -*- coding: utf-8
#**** AUTHOR: - DI0NJ@CK - (compatible with Python 3.7.x)
__author__      = 'Di0nj@ck'
__version__     = 'v1'
__last_update__ = 'January 2020'

import os,sys,re,time,argparse,json,requests,datetime

#GLOBAL VARIABLES
input_file = ""
output_file = "results.json"
results_list = []
viewdns_free_api_key = "PUT_YOUR_API_KEY_HERE"
output_type = "json"

#FUNCTIONS

def reader(path):
    try:
        lines_list = []

        with open(path, 'r+', encoding="utf-8") as f:
            lines = filter(None, (line.rstrip() for line in f))
            for a_line in lines:
                if not a_line.startswith('#'): #FILTER OUT FILE COMMENTS
                    lines_list.append(a_line.strip('\n')) #DELETE NEWLINE CHARACTERS 
        return lines_list
    except:
        return False

def load_json(path):
    try:
        return json.loads(reader(path))
    except:
	    return {}

def write_json(path, data):
    with open(path, 'a') as file:
        json.dump(data, file, indent=4)

def run_api_viewdns(ips_list,api_key,output):
    responses_list = []
    i = 0

    for ip in ips_list:
        i += 1 
        print('     [%i/%i] %s\n' % (i,len(ips_list),str(ip)))
        result = requests.get('https://api.viewdns.info/reverseip/?host=%s&apikey=%s&output=%s' % (ip,api_key,output)) #LIMITED TO 250 QUERIES PER DAY
        result_info = json.loads(result.text)
        responses_list.append(result_info)
    
    return responses_list

def save_results(results_list,output_file):

    for result in results_list:
        write_json(output_file,result)


# *** MAIN CODE ***
if __name__ == '__main__': #MAIN CODE STARTS HERE

    #ARG PARSER
    description =  "Massive Reverser IP - {__author__}"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_file", help='path of input file with an IP on each line')
    parser.add_argument('-v', help='displays the current version', action='version', version=__version__)
    args = parser.parse_args()

    #PARSE IPs IN INPUT FILE
    print('[+] Starting Massive Reverse IP [{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()))
    ips_list = reader(args.input_file)
    print(' [*] Analyzing %i IPs\n' % len(ips_list))

    #REQUEST VIEWDNS FREE API (limited to 250 queries per day)
    print(' [*] Querying ViewDNS Free API (limited to 250 daily quota)...\n')
    results_list = run_api_viewdns(ips_list,viewdns_free_api_key,output_type)

    #WRITE ALL RESULTS INTO A SINGLE JSON FILE
    print(' [*] Saving all results into a single JSON file...\n')
    save_results(results_list,output_file)

    #FINISH
    print(' [*] FINISHED. All done!\n')