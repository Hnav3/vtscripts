import vt
import os, sys, csv, argparse, configparser
from ratelimit import limits, sleep_and_retry

script_path = os.path.dirname(os.path.realpath(__file__))
config=configparser.ConfigParser()
config.read(f'{script_path}/config.ini')

## Rate Limiting. Public API only allows 4 lookups/min
CALLS = config.getint('API','API_CALLS')
RATE_LIMIT=config.getint('API','API_RATE')

CSV_OBJ=[]

def open_vt_session(apikey):
    client = vt.Client(apikey)
    return client

def close_vt_session(client):
    client.close()

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    return

def get_vt_file_obj(client,hash,AV_ENGINES):
    try:
        file = client.get_object(f'/files/{hash}')
        print(f"Getting info for {hash}")
        for av in AV_ENGINES:
            file_obj = {'hash':hash,'file_type':file.exiftool['FileTypeExtension'],'av_engine':file.last_analysis_results[av]['engine_name'],'av_category':file.last_analysis_results[av]['category'],'av_signature':file.last_analysis_results[av]['result']}
            CSV_OBJ.append(file_obj)
    except:
        print(f"Unable to get info for {hash}")
        file_obj = {'hash':f'{hash} NOT FOUND'}
        CSV_OBJ.append(file_obj)

def csv_writer(filename):
    csv_fields = ['hash','file_type','av_engine','av_category','av_signature']

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(CSV_OBJ)

def arg_parse():
    parser = argparse.ArgumentParser("VirusTotal hash lookup tool.")
    parser.add_argument("-i", "--infile", help="CSV File of hashes to search.")
    parser.add_argument("-v", "--value", type=str, help="Hash you'd like to search.")
    parser.add_argument("-s", "--save", type=str, help="Save the CSV file with a different filename.")
    return parser

def main(args):
    if not args.infile and not args.value:
        print("Input file or individual hash is required to run this tool")
        sys.exit()
    elif args.infile and args.value:
        print("Input file and individual hash were provided. Please choose one.")
        sys.exit()
    else:
        filename = args.save or "lookupresults.csv"
        client = open_vt_session(config.get('API','API_KEY'))
        AV_ENGINES = config.get('AV','ENGINES').split(',')
        if args.value:
           check_limit()
           results = get_vt_file_obj(client,args.value,AV_ENGINES)
        else:
           with open(args.infile, 'r') as read_obj:
               csv_reader = csv.DictReader(read_obj)
               for row in csv_reader:
                   check_limit()
                   get_vt_file_obj(client,row['hash'],AV_ENGINES)
        csv_writer(filename)
        close_vt_session(client)

if __name__ == '__main__':
    parser = arg_parse()
    args = parser.parse_args()

    main(args)
