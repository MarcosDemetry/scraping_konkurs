from pathlib import Path
import os,  requests, time, re 
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


# Lists to fill
names = []

links = []
orgnrs = []

dates = []
orts = []

failed = []


months = ['januari', 'februari', 'mars', 'april', 'maj']
year = '2020'

for month in months:
    ## Reading in files
    file = str(datadir) + "/" + str(year) + str(month) + "_data.htm"
    infile = open(file, 'rb')
    text = infile.read()
    soup = BeautifulSoup(text, 'lxml')

    # Parsing
    maincontainer = soup.find('table', attrs = {'class' : 'table table-sm table-striped'})

    rows = maincontainer.find_all('tr')
    print(len(rows))

    for row in rows:
        try:
            # Extracting
            name = row.find('a')
            link = row.a['href']
            orgnr = re.search(r'\d+', link)[0]

            link = "https://kreditrapporten.se" + str(link)

            info1 = row.find_all('div')[0]
            info2 = row.find_all('div')[1]
            
            date = re.search(r'\d{4}-\d{2}-\d{2}', str(info1))[0]
            ort = re.search(r'\d{4}-\d{2}-\d{2} - (.+)<', str(info1))[1]
            if ort and date is not None:
                orts.append(ort)
                dates.append(date)
            else:
                orts.append("")
                dates.append("")

            # Filling in lists
            names.append(name.get_text())
            links.append(link)
            orgnrs.append(orgnr)


        except:
            print("Couldn't parse firm {}.".format(orgnr))
            failed.append(row)

df = pd.DataFrame({'name'   :   names,
                   'link'   :   links,
                   'orgnr'  :   orgnrs,
                   'date'   :   dates,
                   'ort'    :   orts})

