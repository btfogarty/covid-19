# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:46:55 2020

@author: vtfog
"""

import pandas

#get data from git
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
confirmed = pandas.read_csv(url,error_bad_lines=False)

print(confirmed.head())

url = 'https://github.com/btfogarty/covid-19/tree/master/data/test.csv'
confirmed.to_csv(url)

