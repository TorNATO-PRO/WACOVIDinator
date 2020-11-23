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

# This program parses COVID-19 data from the Washington State Department of Health
# I DON'T OWN THE DATA

# native libraries
import os
from datetime import datetime

# foreign libraries
import connectionchecker as cc
import dataparser as dp
import requests

# program introduction
print('                           )        (   (      ')
print(' (  (      (         (  ( /(        )\\ ))\\ )   ')
print(' )\\))(    )\\        )\\ )\\())(   ( (()/(()/(   ')
print('((_)()\\ |(((_)(    (((_|(_)\\ )\\  )\\ /(_))(_))  ')
print('_(())\\_)()\\ _ )\\   )\\___ ((_|(_)((_|_))(_))_   ')
print('\\ \\((_)/ (_)_\\(_) ((/ __/ _ \\ \\ / /|_ _||   \\  ')
print(' \\ \\/\\/ / / _ \\    | (_| (_) \\ V /  | | | |) | ')
print('  \\_/\\_/ /_/ \\_\\    \\___\\___/ \\_/  |___||___/  ')

onlineupdate = 'unknown'
if cc.hasconnection():
    onlinedatasetinfo = requests.head('https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables'
                                      '/PUBLIC_CDC_Event_Date_SARS.xlsx')
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
else:
    if os.path.isfile('PUBLIC_CDC_Event_Date_SARS.xlsx'):
        print('As there is no connection detected, proceeding to next part of the program')
    else:
        quit()


dp.stateinfoparser(onlineupdate)

# "main" method
while True:
    county = input('\nPlease enter a Washington county: ')
    if county == 'quit' or county == 'q':
        quit()

    print('Do you want Hospitalization, Cases, or Death data?')
    action = input('\nWhat data do you want: ')

    if action.capitalize().__contains__('H'):
        dp.hospplot(county)
    elif action.capitalize().__contains__('C'):
        dp.caseplot(county)
    elif action.capitalize().__contains__('D'):
        dp.deathplot(county)
    else:
        print('Invalid input!')

    dp.countyinfoparser(county, onlineupdate)
