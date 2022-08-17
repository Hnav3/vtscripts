import vt
import os, sys, csv, argparse, configparser

script_path = os.path.dirname(os.path.realpath(__file__))
config=configparser.ConfigParser()
config.read(f'{script_path}/config.ini')

def open_vt_session(apikey):
    client = vt.Client(apikey)
    return client

def close_vt_session(client):
    client.close()

def get_vt_engines(client):
    try:
        metadata = client.get_json('/metadata')
        for e in metadata['data']['engines']:
            print(e)

    except:
        print("Unable to grab AV Engines")
        


def arg_parse():
    parser = argparse.ArgumentParser("VirusTotal hash lookup tool.")
    return parser

def main(args):
    client = open_vt_session(config.get('API','API_KEY'))
    get_vt_engines(client)
    close_vt_session(client)

if __name__ == '__main__':
    parser = arg_parse()
    args = parser.parse_args()

    main(args)
