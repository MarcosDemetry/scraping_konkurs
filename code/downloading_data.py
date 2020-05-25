###############
### Konkurs ###
###############

from pathlib import Path
import os,  requests, time,re 
from random import randint
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup

## Setting CWD
cwd = os.getcwd()
root = Path(cwd).parents[0]
datadir = str(Path(root)) + str('/data')
outputdir = str(Path(root)) + str('/output')
print("Root: " + str(root))

## https://kreditrapporten.se/konkurser-april-2020

### For scraping
HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}

# Lists to loop over
months = ['januari', 'februari', 'mars', 'april', 'maj']
years = ['2020']


# General
start_time = time.time()

nr_requests = 0

failed = []

## Main loop
for year in years:
    for month in months:
        try:
            url = "https://kreditrapporten.se/konkurser-" + str(month) + "-" + str(year)
            res = requests.get(url, timeout = 5, headers = HEADERS)
            print(res)

            time.sleep(randint(10,20))

            nr_requests += 1
            elapsed_time = time.time() - start_time
            print("Requests: {}; Frequency: {} requests/s.".format(nr_requests, nr_requests/elapsed_time))

            # Saving copy of webpage
            file = str(datadir) + "/" + str(year) + str(month) + "_data.htm"
            outfile = open(file, 'wb')
            for chunk in res.iter_content(10):
                  outfile.write(chunk)
            outfile.close()
                            
        except:
            print("Couldn't get info on {} {}.".format(month, year))
            X = str(month) + str(year)
            failed.append(X)

