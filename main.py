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

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import requests


class WAPop:
    washingtonPopulation = 7614893

    countypopulation = {
        'King County': 2252782,
        'Pierce County': 904980,
        'Snohomish County': 822083,
        'Spokane County': 522798,
        'Clark County': 488231,
        'Thurston County': 290536,
        'Kitsap County': 271473,
        'Yakima County': 250873,
        'Whatcom County': 229247,
        'Benton County': 204390,
        'Skagit County': 129205,
        'Cowlitz County': 110593,
        'Grant County': 97733,
        'Franklin County': 95222,
        'Island County': 85141,
        'Lewis County': 80707,
        'Clallam County': 77331,
        'Chelan County': 77200,
        'Grays Harbor County': 75061,
        'Mason County': 66768,
        'Walla Walla County': 60760,
        'Whitman County': 50104,
        'Kittitas County': 47935,
        'Stevens County': 45723,
        'Douglas County': 43429,
        'Okanogan County': 42243,
        'Jefferson County': 32221,
        'Asotin County': 22582,
        'Pacific County': 22471,
        'Klickitat County': 22425,
        'Adams County': 19983,
        'San Juan County': 17582,
        'Pend Oreille County': 13724,
        'Skamania County': 12083,
        'Lincoln County': 10939,
        'Ferry County': 7627,
        'Wahkiakum County': 4488,
        'Columbia County': 3985,
        'Garfield County': 2225
    }


population = WAPop()

# fun style
plt.style.use('ggplot')

print('*********************')
print('*COVID-19 Visualizer*')
print('*********************\n')

onlinedatasetinfo = requests.head('https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables'
                                  '/PUBLIC_CDC_Event_Date_SARS.xlsx?ver=20201121144748')

onlineupdate = datetime.strptime(onlinedatasetinfo.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT')

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
cases = pd.read_excel(excelFile, 'Cases',
                      usecols=['WeekStartDate', 'NewPos_All', 'County'],
                      parse_dates=['WeekStartDate'])
deaths = pd.read_excel(excelFile, 'Deaths',
                       usecols=['WeekStartDate', 'Deaths', 'County'],
                       parse_dates=['WeekStartDate'])
hospitalizations = pd.read_excel(excelFile, 'Hospitalizations',
                                 usecols=['WeekStartDate', 'Hospitalizations', 'County'],
                                 parse_dates=['WeekStartDate'])
cases.set_index('WeekStartDate', inplace=True)
deaths.set_index('WeekStartDate', inplace=True)
knownhosp = hospitalizations[hospitalizations['WeekStartDate'] != 'Unknown']
knownhosp.set_index('WeekStartDate', inplace=True)
hospitalizations.set_index('WeekStartDate', inplace=True)


# computes death to case ratio
def ratioer(fatalities, positives):
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


totalwacase = cases['NewPos_All'].sum()
totalwadeath = deaths['Deaths'].sum()
totalwahosp = hospitalizations['Hospitalizations'].sum()
wadtr = ratioer(totalwadeath, totalwacase)

print('Total YTD deaths in Washington as of ' + str(onlineupdate) + ': ' + str(totalwadeath))
print('Total YTD cases in Washington as of ' + str(onlineupdate) + ': ' + str(totalwacase))
print('Total YTD hospitalizations in Washington as of ' + str(onlineupdate) + ': ' + str(totalwahosp))
print('Death to population ratio as of ' + str(onlineupdate) + ': ' + str(totalwadeath /
                                                                          population.washingtonPopulation))
print('YTD Hospitalization to case ratio in Washington as of ' + str(onlineupdate) + ': ' +
      str(ratioer(totalwahosp, totalwacase)))
print('YTD Hospitalization to death ratio in Washington as of ' + str(onlineupdate) + ': ' +
      str(ratioer(totalwahosp, totalwadeath)))
print('Case to population ratio as of ' + str(onlineupdate) + ': ' + str(totalwacase /
                                                                         population.washingtonPopulation))
print('Hospitalization to population ratio as of ' + str(onlineupdate)
      + ': ' + str(totalwahosp /
      population.washingtonPopulation))
print('Death to case ratio in Washington as of ' + str(onlineupdate) + ': ' + str(wadtr))

# "main" method
while True:
    county = input('\nPlease enter a Washington county: ')
    if county == 'quit' or county == 'q':
        break

    countycase = cases.loc[cases['County'] == county]
    countydeath = deaths.loc[deaths['County'] == county]
    countyhosp = knownhosp.loc[knownhosp['County'] == county]  # verified
    countytruehosp = hospitalizations.loc[hospitalizations['County'] == county]  # total known and unknown dates

    sumDeaths = countydeath['Deaths'].sum()
    sumCases = countycase['NewPos_All'].sum()
    sumHosp = countytruehosp['Hospitalizations'].sum()
    print('Total YTD cases in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(sumCases))
    print('Total YTD deaths in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(sumDeaths))
    print('YTD Death to case ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        ratioer(sumDeaths, sumCases)))
    print('YTD Hospitalization to case ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        ratioer(sumHosp, sumCases)))
    print('YTD Hospitalization to death ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        ratioer(sumHosp, sumDeaths)))
    print('YTD Case to population ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        ratioer(sumCases, population.countypopulation[county])))
    print('YTD Death to population ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        ratioer(sumDeaths, population.countypopulation[county])))
    print('YTD Hospitalization to population ratio in ' + county + ' as of ' + str(onlineupdate) + ': ' + str(
        ratioer(sumHosp, population.countypopulation[county])))

    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    ax1 = fig.add_subplot(gs[0, 0])
    makeplot(ax1, countycase.index, countycase['NewPos_All'], 'Cases', 'crimson')
    ax2 = fig.add_subplot(gs[1, :])
    makeplot(ax2, countydeath.index, countydeath['Deaths'], 'Deaths', 'lime')
    ax3 = fig.add_subplot(gs[0, 1])
    makeplot(ax3, countyhosp.index, countyhosp['Hospitalizations'], 'Hospitalizations', 'darkblue')

    fig.suptitle('COVID-19 Data in ' + county, fontsize=16)
    plt.show()