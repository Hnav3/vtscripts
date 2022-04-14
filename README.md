# VTScripts

## Install
Install requirements.txt

<code>pip install -r requirements.txt</code>

## hashlookup.py
<code>python hashlookup.py</code>

Will dump to cwd/lookup.csv

### Config
#### AV Engines
Edit the AV_ENGINES variable to tell the script which AV engine you're trying to verify against.
*https://support.virustotal.com/hc/en-us/articles/115002146809-Contributors

#### API Rate Limiting
On VirusTotal, go to your Account > API Key. Request rate will tell you what your quota is. 4 lookups/min is the default for free accounts.
* CALLS = 4
* RATE_LIMIT=60
