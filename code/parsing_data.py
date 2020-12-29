####################
### Parsing Data ###
####################

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

infos1 = []
dates = []
orts = []

infos2 = []

infos3 = []
revenues =[]
employees = []

failed = []

months = ['januari', 'februari', 'mars', 'april', 'maj', 'juni', 'juli','augusti', 'september', 'oktober', 'november']
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
            info3 = row.find_all('div')[2]

            # Filling in lists
            names.append(name.get_text())
            links.append(link)
            orgnrs.append(orgnr)
            infos1.append(info1)
            infos2.append(info2)
            infos3.append(info3)

        except:
            print("Couldn't parse firm {}.".format(orgnr))
            failed.append(row)

# Saving df
df = pd.DataFrame({'name'       :   names,
                   'link'       :   links,
                   'orgnr'      :   orgnrs,
                   'info1'      :   infos1,
                   'info2'      :   infos2,
                   'info3'      :   infos3})

outfile = str(datadir) + "/raw_konkurs_data.csv"
df.to_csv(outfile)

# Cleaning df
file = str(datadir) + "/raw_konkurs_data.csv"
df = pd.read_csv(file, index_col=0)

df['date'] = df['info1'].str.extract(r'(\d{4}-\d{2}-\d{2})')
df['ort'] = df['info1'].str.extract(r'\d{4}-\d{2}-\d{2} - .+>(.+)</span>')

df['municipality'] = df['info2'].str.extract(r'säte i .+>(.+)</span>')

df['revenue'] = df['info3'].str.extract(r'Omsättning.+ ((\d{1,3})? (\d{1,3}) (t?kr))')[0]
df['employees'] = df['info3'].str.extract(r'((\d{1,3})? (\d{1,3})) anställda')[0]

df.drop(['info1', 'info2', 'info3'], axis=1, inplace=True)

outfile = str(datadir) + "/clean_konkurs_data.csv"
df.to_csv(outfile, index=False)
