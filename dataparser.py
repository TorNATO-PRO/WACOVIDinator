#  Copyright (c) waltz 2020.
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

import matplotlib.pyplot as plt
import pandas as pd
import wapop as wp

# reading the file's data
excelFile = pd.ExcelFile('PUBLIC_CDC_Event_Date_SARS.xlsx')
cases = pd.read_excel(excelFile, 'Cases',
                      usecols=['WeekStartDate', 'NewPos_All', 'County'],
                      parse_dates=['WeekStartDate'])
deaths = pd.read_excel(excelFile, 'Deaths',
                       usecols=['WeekStartDate', 'Deaths', 'County'],
                       parse_dates=['WeekStartDate'])
hospitalizations = pd.read_excel(excelFile, 'Hospitalizations',
                                 usecols=['WeekStartDate', 'Hospitalizations', 'County'])

# cleansing the data
knownhosp = hospitalizations[hospitalizations['WeekStartDate'] != 'Unknown']
plothosp = knownhosp.copy()
plothosp['County'] = knownhosp['County'].astype('category')
plothosp['WeekStartDate'] = knownhosp['WeekStartDate'].astype('datetime64')
plotdeath = deaths.copy()
plotdeath['County'] = deaths['County'].astype('category')
plotdeath['WeekStartDate'] = deaths['WeekStartDate'].astype('datetime64')
plotcase = cases.copy()
plotcase['County'] = cases['County'].astype('category')
plotcase['WeekStartDate'] = cases['WeekStartDate'].astype('datetime64')

# important values
totalhosp = hospitalizations['Hospitalizations'].sum()
totaldeath = deaths['Deaths'].sum()
totalcase = cases['NewPos_All'].sum()


def hospplot(county):
    ylabel = 'Hospitalizations'
    countyhosp = plothosp.loc[plothosp['County'] == county]
    ax = countyhosp.plot(x='WeekStartDate',
                         y=ylabel,
                         kind='line',
                         title='COVID-19 ' + ylabel + ' in ' + county,
                         color='tab:red')
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    plt.show()


def deathplot(county):
    ylabel = 'Deaths'
    countydeath = plotdeath.loc[plotdeath['County'] == county]
    ax = countydeath.plot(x='WeekStartDate',
                          y=ylabel,
                          kind='line',
                          title='COVID-19 ' + ylabel + ' in ' + county,
                          color='tab:purple')
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    plt.show()


def caseplot(county):
    ylabel = 'Cases'
    countycase = plotcase.loc[plotcase['County'] == county]
    ax = countycase.plot(x='WeekStartDate',
                          y='NewPos_All',
                          kind='line',
                          title='COVID-19 ' + ylabel + ' in ' + county,
                          color='tab:blue')
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    plt.show()


# includes all confirmed and unconfirmed cases
def sumcountycases(county):
    return cases[cases['County'] == county]['NewPos_All'].sum()


# includes all confirmed and unconfirmed deaths
def sumcountydeaths(county):
    return deaths[deaths['County'] == county]['Deaths'].sum()


# includes all confirmed and unconfirmed hospitalizations
def sumcountyhospitalizations(county):
    return hospitalizations[hospitalizations['County'] == county]['Hospitalizations'].sum()


# parses state information
def stateinfoparser(onlineupdate):
    # relevant calculations
    totalwacase = totalcase
    totalwadeath = totaldeath
    totalwahosp = totalhosp
    wadeathtocase = totalwadeath / totalwacase
    wadeathtopop = totalwadeath / wp.washingtonPopulation
    wahosptocase = totalwahosp / totalwacase
    wadeathtohosp = totalwadeath / totalwahosp
    wacasetopop = totalwacase / wp.washingtonPopulation
    wahosptopop = totalwahosp / wp.washingtonPopulation

    # relevant Washington information
    print('Total YTD deaths in Washington as of {0}: {1}'.format(onlineupdate,
                                                                 totalwadeath))
    print('Total YTD cases in Washington as of {0}: {1}'.format(onlineupdate,
                                                                totalwacase))
    print('Total YTD hospitalizations in Washington as of {0}: {1}'.format(onlineupdate,
                                                                           totalwahosp))
    print('Death to population ratio as of {0}: {1:1.3f} ({2:1.3f}%)'.format(onlineupdate,
                                                                             wadeathtopop,
                                                                             wadeathtopop * 100))
    print('YTD Hospitalization to case ratio in Washington as of {0}: {1:1.3f} ({2:1.3f}%)'.format(onlineupdate,
                                                                                                   wahosptocase,
                                                                                                   wahosptocase * 100))
    print('YTD death to hospitalization ratio in Washington'
          ' as of {0}: {1:1.3f} ({2:1.3f}%)'.format(onlineupdate,
                                                    wadeathtohosp,
                                                    wadeathtohosp * 100))
    print('Case to population ratio as of {0}: {1:1.3f} ({2:1.3f}%)'.format(onlineupdate, wacasetopop,
                                                                            wacasetopop * 100))
    print('Hospitalization to population ratio as of {0}: {1:1.3f} ({2:1.3f}%)'.format(onlineupdate, wahosptopop,
                                                                                       wahosptopop * 100))
    print('Death to case ratio in Washington as of {0}: {1:1.3f} ({2:1.3f}%)'.format(onlineupdate, wadeathtocase,
                                                                                     wadeathtocase * 100))


# parses county info
def countyinfoparser(county, onlineupdate):
    sumdeath = sumcountydeaths(county)
    sumcases = sumcountycases(county)
    sumhosp = sumcountyhospitalizations(county)
    deathtocase = sumdeath / sumcases
    hosptocase = sumhosp / sumcases
    deathtohosp = sumdeath / sumhosp

    countypopulation = wp.countypopulation[county]

    casetopop = sumcases / countypopulation
    deathtopop = sumdeath / countypopulation
    hosptopop = sumhosp / countypopulation
    # displays relevant data
    print('Total YTD cases in {0} as of {1}: {2}'.format(county, onlineupdate, sumcases))
    print('Total YTD deaths in {0} as of {1}: {2}'.format(county, onlineupdate, sumdeath))
    print('Total YTD hospitalizations in {0} as of {1}: {2}'.format(county, onlineupdate, sumhosp))
    print('YTD Death to case ratio in {0} as of {1}: {2:1.3f} ({3:1.3f}%)'.format(county,
                                                                                  onlineupdate,
                                                                                  deathtocase,
                                                                                  deathtocase * 100))
    print('YTD Hospitalization to case ratio in {0} as of {1}: {2:1.3f} ({3:1.3f}%)'.format(county,
                                                                                            onlineupdate,
                                                                                            hosptocase,
                                                                                            hosptocase * 100))
    print('YTD death to hospitalization ratio in {0} as of {1}: {2:1.3f} ({3:1.3f}%)'.format(county,
                                                                                             onlineupdate,
                                                                                             deathtohosp,
                                                                                             deathtohosp * 100))
    print('YTD Case to population ratio in {0} as of {1}: {2:1.3f} ({3:1.3f}%)'.format(county,
                                                                                       onlineupdate,
                                                                                       casetopop,
                                                                                       casetopop * 100))
    print(
        'YTD Death to population ratio in {0} as of {1}: {2:1.3f} ({3:1.3f}%)'.format(county,
                                                                                      onlineupdate,
                                                                                      deathtopop,
                                                                                      deathtopop * 100))
    print('YTD Hospitalization to population ratio in {0} as of {1}'
          ': {2:1.3f} ({3:1.3f}%)'.format(county,
                                          onlineupdate,
                                          hosptopop,
                                          hosptopop * 100))
