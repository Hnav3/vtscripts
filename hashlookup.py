import vt
import os, sys, csv, argparse
from ratelimit import limits, sleep_and_retry

script_path = os.path.dirname(os.path.realpath(__file__))

AV_ENGINES = ['AV1','AV2','AV3']
CSV_FILE=f'{script_path}/lookup.csv'
CSV_OBJ=[]

## Rate Limiting. Public API only allows 4 lookups/min
CALLS = 4
RATE_LIMIT=60

def open_vt_session(apikey):
    client = vt.Client(apikey)
    return client

def close_vt_session(client):
    client.close()

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    return

def get_vt_file_obj(client,hash):
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

def csv_writer():
    csv_fields = ['hash','file_type','av_engine','av_category','av_signature']

    with open(CSV_FILE, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(CSV_OBJ)

def main():
    parser = argparse.ArgumentParser("VirusTotal hash lookup tool.")
    parser.add_argument("--apikey", required=True, help="API Key from VirusTotal.com.")
    parser.add_argument("--infile", help="CSV File of hashes to search.")
    parser.add_argument("--hash", help="Hash you'd like to search.")
    args = parser.parse_args()

    if not args.infile and not args.hash:
        print("Input file or individual hash is required to run this tool")
        sys.exit()
    elif args.infile and args.hash:
        print("Input file and individual hash were provided. Please choose one.")
        sys.exit()
    else:
        client = open_vt_session(args.apikey)
        if args.hash:
           check_limit()
           get_vt_file_obj(client,args.hash)
        else:
           with open(args.infile, 'r') as read_obj:
               csv_reader = csv.DictReader(read_obj)
               for row in csv_reader:
                   check_limit()
                   get_vt_file_obj(client,row['hash'])
        csv_writer()
        close_vt_session(client)

if __name__ == '__main__':
   sys.exit(main())
