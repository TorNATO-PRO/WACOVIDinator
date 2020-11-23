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

import requests


# checks internet connection
def hasconnection():
    url = 'https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/'
    timeout = 5
    print('Checking internet connection')
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("Internet is currently down!")
        return False
