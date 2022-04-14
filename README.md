# VTScripts

## Install
Install requirements.txt

<code>pip install -r requirements.txt</code>

## hashlookup.py
<code>
usage: VirusTotal hash lookup tool. [-h] [-i INFILE] [-v VALUE] [-s SAVE]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        CSV File of hashes to search.
  -v VALUE, --value VALUE
                        Hash you'd like to search.
  -s SAVE, --save SAVE  Save the CSV file with a different filename.
</code>

Will dump to cwd/lookupresults.csv if no file is specified

### Config
#### AV Engines
Comma separated list of AV Engines.
* https://support.virustotal.com/hc/en-us/articles/115002146809-Contributors

#### API
On VirusTotal, go to your Account > API Key. Request rate will tell you what your quota is. 4 lookups/min is the default for free accounts.
* API_KEY 
* CALLS
* RATE_LIMIT
