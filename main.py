#  Copyright (c) Nathan Waltz 2020.
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests

# fun style
plt.style.use('fivethirtyeight')

print('*********************')
print('*COVID-19 Visualizer*')
print('*********************\n')

onlinedatasetinfo = requests.head('https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables'
                                  '/PUBLIC_CDC_Event_Date_SARS.xlsx?ver=20201121144748')
onlineupdate = datetime.strptime(onlinedatasetinfo.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT')

# automated file updating
if os.path.isfile('PUBLIC_CDC_Event_Date_SARS.xlsx'):
    downloaded = os.stat('PUBLIC_CDC_Event_Date_SARS.xlsx').st_mtime
    if onlineupdate > datetime.fromtimestamp(downloaded):  # if the online version is newer
        print('Dataset is out of date, deleting the old file!')
        os.remove('PUBLIC_CDC_Event_Date_SARS.xlsx')
        print('Downloading new dataset')
        downloadedFile = requests.get('https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables'
                                      '/PUBLIC_CDC_Event_Date_SARS.xlsx?ver=20201121144748')
        open('PUBLIC_CDC_Event_Date_SARS.xlsx', 'wb').write(downloadedFile.content)
        print('Dataset downloaded successfully')
    else:
        print('File is already updated and exists!')
else:
    print('Dataset does not yet exist, proceeding to download!')
    downloadedFile = requests.get('https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables'
                                  '/PUBLIC_CDC_Event_Date_SARS.xlsx?ver=20201121144748')
    open('PUBLIC_CDC_Event_Date_SARS.xlsx', 'wb').write(downloadedFile.content)

# reading the file's data
excelFile = pd.ExcelFile('PUBLIC_CDC_Event_Date_SARS.xlsx')
cases = pd.read_excel(excelFile, 'Cases')
deaths = pd.read_excel(excelFile, 'Deaths')


# computes death to case ratio
def deathtocase(fatalities, positives):
    return fatalities / positives


# "main" method
while True:

    totalwacase = cases['NewPos_All'].sum()
    totalwadeath = deaths['Deaths'].sum()
    wadtr = deathtocase(totalwadeath, totalwacase)

    print('Total YTD deaths in Washington as of ' + str(onlineupdate) + ': ' + str(totalwadeath))
    print('Total YTD cases in Washington as of ' + str(onlineupdate) + ': ' + str(totalwacase))
    print('Death to case ratio in Washington as of ' + str(onlineupdate) + ': ' + str(wadtr))

    county = input('Please enter a Washington county: ')
    if county == 'quit' or county == 'q':
        break

    countycase = cases.loc[cases['County'] == county]
    countydeath = deaths.loc[deaths['County'] == county]
    countyhospitalizations = deaths.loc[deaths['County'] == county]

    sumDeaths = countydeath['Deaths'].sum()
    sumCases = countycase['NewPos_All'].sum()
    print('Total YTD cases in ' + county + ': ' + str(sumCases))
    print('Total YTD deaths in ' + county + ': ' + str(sumDeaths))
    print('Death to case ratio in ' + county + ': ' + str(deathtocase(sumDeaths, sumCases)))

    fig, ax = plt.subplots()
    ax.plot(countycase['WeekStartDate'], countycase['NewPos_All'], label='Cases', c='crimson')
    ax.plot(countydeath['WeekStartDate'], countydeath['Deaths'], label='Deaths', c='lime')
    ax.legend()

    every_nth = 6
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.title('Weekly COVID-19 Cases and Deaths in ' + county, fontsize='small')
    plt.xlabel('Date', fontsize='small')
    plt.ylabel('Number of People', fontsize='small')
    plt.show()