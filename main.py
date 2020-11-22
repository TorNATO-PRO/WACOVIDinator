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
import matplotlib.gridspec as gridspec
import pandas as pd
import requests

# fun style
plt.style.use('ggplot')

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
        print('Dataset is already updated and exists!')
else:
    print('Dataset does not yet exist, proceeding to download!')
    downloadedFile = requests.get('https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables'
                                  '/PUBLIC_CDC_Event_Date_SARS.xlsx?ver=20201121144748')
    open('PUBLIC_CDC_Event_Date_SARS.xlsx', 'wb').write(downloadedFile.content)

# reading the file's data
excelFile = pd.ExcelFile('PUBLIC_CDC_Event_Date_SARS.xlsx')
cases = pd.read_excel(excelFile, 'Cases')
deaths = pd.read_excel(excelFile, 'Deaths')
hospitalizations = pd.read_excel(excelFile, 'Hospitalizations')


# computes death to case ratio
def deathtocase(fatalities, positives):
    return fatalities / positives


def setticks(ax, every_nth):
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)


def makeplot(ax, xcoord, ycoord, name, color):
    ax.plot(xcoord, ycoord, label=name, c=color)
    ax.legend()
    ax.set(xlabel='Date', ylabel='# of people')
    setticks(ax, 9)


# "main" method
while True:
    totalwacase = cases['NewPos_All'].sum()
    totalwadeath = deaths['Deaths'].sum()
    wadtr = deathtocase(totalwadeath, totalwacase)

    print('Total YTD deaths in Washington as of ' + str(onlineupdate) + ': ' + str(totalwadeath))
    print('Total YTD cases in Washington as of ' + str(onlineupdate) + ': ' + str(totalwacase))
    print('Death to case ratio in Washington as of ' + str(onlineupdate) + ': ' + str(wadtr))

    county = input('\n\nPlease enter a Washington county: ')
    if county == 'quit' or county == 'q':
        break

    countycase = cases.loc[cases['County'] == county]
    countydeath = deaths.loc[deaths['County'] == county]
    countyhosp = hospitalizations.loc[hospitalizations['County'] == county]

    sumDeaths = countydeath['Deaths'].sum()
    sumCases = countycase['NewPos_All'].sum()
    print('Total YTD cases in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(sumCases))
    print('Total YTD deaths in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(sumDeaths))
    print('Death to case ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        deathtocase(sumDeaths, sumCases)))

    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    ax1 = fig.add_subplot(gs[0, 0])
    makeplot(ax1, countycase['WeekStartDate'], countycase['NewPos_All'], 'Cases', 'crimson')
    ax2 = fig.add_subplot(gs[0, 1])
    makeplot(ax2, countydeath['WeekStartDate'], countydeath['Deaths'], 'Deaths', 'lime')
    ax3 = fig.add_subplot(gs[1, :])
    makeplot(ax3, countyhosp['WeekStartDate'], countyhosp['Hospitalizations'], 'Hospitalizations', 'darkblue')

    fig.suptitle('COVID-19 Data in ' + county, fontsize=16)
    plt.show()
    print('\n\n\n')