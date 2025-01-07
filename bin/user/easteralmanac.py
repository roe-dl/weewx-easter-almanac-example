#!/usr/bin/python3
# Almanac extension to WeeWX for calculating easter date
# Copyright (C) 2025 Johanna Roedenbeck

"""

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

"""
    This is an example how to write an almanac extension for WeeWX. It
    provides the date of the easter sunday calculated by the formula
    of Carl Friedrich Gauß.
    
    Put in your skin:
    `$almanac.easter.format('%Y-%m-%d')`
    `$almanac(almanac_time=time).easter.format('%Y-%m-%d')`

    Replace the format string by the date format of your choice.
        
    As this is an example, it is simple. One attribute is calculated
    only. A real world extension would provide a `next_easter` and
    `previous_easter` attribute as well. 
"""

VERSION = "0.1"

import time
import datetime

import weewx
from weewx.almanac import AlmanacType, almanacs
from weewx.engine import StdService
from weewx.units import ValueTuple, ValueHelper


def calc_easter_date(year, gregorian):
    """ calculate the day of March of the easter sunday """
    # Source: https://de.wikipedia.org/wiki/Gaußsche_Osterformel
    # formula according to Heiner Lichtenberg
    if gregorian:
        # Ausnahmen aus politischen Gruenden
        if year==1724: return 40
        if year==1744: return 29
    # die Saekularzahl
    K = (year-year%100)/100
    # die saekulare Mondschaltung
    K3 = 3*K+3
    K3 = (K3-K3%4)/4
    K8 = 8*K+13
    K8 = (K8-K8%25)/25
    M = 15+K3-K8
    # die saekulare Sonnenschaltung
    S = 2-K3
    # julianischer Kalender vor 1700
    if not gregorian:
        M = 15
        S = 0
    # den Mondparameter
    A = year%19
    # den Keim fuer den ersten Vollmond im Fruehling
    D = (19*A+M)%30
    # die kalendarische Korrekturgroesze
    R = D+(A-A%11)/11
    R = (R-R%29)/29
    # die Ostergrenze
    OG = 21+D-R
    # den ersten Sonntag im Maerz
    SZ = 7-(year+(year-year%4)/4+S)%7
    # die Entfernung des Ostersonntages von der Ostergrenze
    OE = 7-(OG-SZ)%7
    # das Datum des Ostersonntages als Maerzdatum
    return OG+OE


class EasterAlmanac(AlmanacType):
    """ Almanac extension to provide the date of the Easter sunday """

    def get_almanac_data(self, almanac_obj, attr):
        if attr=='easter':
            # get the actual timestamp
            ti = time.localtime(almanac_obj.time_ts)
            # calculate the easter date of the year of the timestamp
            easter_mday = calc_easter_date(ti.tm_year,True)
            easter_mon = 3
            # If the day is more than 31, the day is in April. So add 1 to
            # the month and subtract 31 from the day.
            if easter_mday>31:
                easter_mday -= 31
                easter_mon += 1
            # Make a timestamp out of it
            easter = datetime.datetime.fromisoformat(
              '%04d-%02d-%02dT12:00:00Z' % (ti.tm_year,easter_mon,easter_mday))
            # Convert to ValueTuple
            vt = ValueTuple(easter.timestamp(),'unix_epoch','group_time')
            # Embed in ValueHelper
            vh = ValueHelper(vt,
                             context='ephem_year',
                             formatter=almanac_obj.formatter,
                             converter=almanac_obj.converter)
            return vh
        # `attr` is not provided by this extension. So raise an exception.
        raise weewx.UnknownType


class EasterService(StdService):
    """ Service to initialize the Easter almanac extension """

    def __init__(self, engine, config_dict):
        # instantiate the Easter almanac
        self.easter_almanac = EasterAlmanac()
        # add to the list of almanacs
        almanacs.insert(0,self.easter_almanac)
    
    def shutDown(self):
        # find the Easter almanac in the list of almanac
        idx = almanacs.index(self.easter_almanac)
        # remove it from the list
        del almanacs[idx]
