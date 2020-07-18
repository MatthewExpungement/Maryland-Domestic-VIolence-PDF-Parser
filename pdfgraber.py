__author__ = 'Matthew'
import requests
from time import sleep
import sys
import os
from datetime import datetime

def getPDF(url,county,name):
    r = requests.get(url, allow_redirects=True)
    if(r.status_code != 200):
        print("Problem with",url)
        sys.exit(0)
    path = county + '\\' + name
    open(path, 'wb').write(r.content)

def makeCountyFolders(counties):
    for county in counties:
        os.mkdir('' + county)

years = ('2020','2019','2018','2017','2016','2015','2014')
counties = (
    'Allegany',
    'Carroll',
    'Harford',
    'Saint_Marys',
    'Anne_Arundel',
    'Cecil',
    'Howard',
    'Somerset',
    'Baltimore_City',
    'Charles',
    'Kent',
    'Talbot',
    'Baltimore',
    'Dorchester',
    'Montgomery',
    'Washington',
    'Calvert',
    'Frederick',
    'Prince_Georges',
    'Wicomico',
    'Caroline',
    'Garrett',
    'Queen_Annes',
    'Worcester'
)

# Used to quickly make all the county folders


today = datetime.today()
curr_month = today.month

for county in counties:
    for year in years:
        for month in range(1,13):
            print("Grabbing",county,year,month)
            # Need to make sure we're not pulling future reports
            if(year == '2020' and month >= curr_month):
                print("Skipping Future Report")
                continue

            # URL Code is DVCR_ + [County] + _[Year]+_[Month]
            url = 'http://jportal.mdcourts.gov/dv/DVCR_'+county+'_'+ year+ '_' + str(month) + '.pdf'
            name = 'DVCR_'+county+'_'+ year+ '_' + str(month) + '.pdf'
            getPDF(url,county,name)
            sleep(1)