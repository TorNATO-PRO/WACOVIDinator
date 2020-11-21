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

import matplotlib.pyplot as plt
# import required libraries
import pandas as pd

# fun style
plt.style.use('dark_background')

excelFile = pd.ExcelFile('PUBLIC_CDC_Event_Date_SARS.xlsx')
cases = pd.read_excel(excelFile, 'Cases')
deaths = pd.read_excel(excelFile, 'Deaths')

print('*********************')
print('*COVID-19 Visualizer*')
print('*********************\n')

while True:
    county = input('Please enter a Washington county: ')
    if county == 'quit' or county == 'q':
        break
    countycase = cases.loc[cases['County'] == county]
    countydeath = deaths.loc[deaths['County'] == county]

    fig, ax = plt.subplots()

    ax.plot(countycase['WeekStartDate'], countycase['NewPos_All'], label='Cases', c='crimson')
    ax.plot(countydeath['WeekStartDate'], countydeath['Deaths'], label='Deaths', c='lime')
    ax.legend()

    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.title('Weekly COVID-19 Cases and Deaths in ' + county)
    plt.xlabel('Date')
    plt.ylabel('Number of People')
    plt.show()