# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:46:55 2020

@author: vtfog
"""

import pandas
import getpass

#parameters
start_day = "1/22/20"
data_out = pandas.DataFrame(columns = ['Province_State','Admin2','Date','Confirmed','Deaths'])

#get data from git (confirmed)
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
confirmed = pandas.read_csv(url,error_bad_lines=False)

#get data from git (confirmed)
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
deaths = pandas.read_csv(url,error_bad_lines=False)

#column range
col = confirmed.columns.get_loc(start_day)
num_cols = len(confirmed.columns)

#loop through all date columns. assumption that all source files have same date columns
while col < num_cols:
    
    #create the daily dataframe slice
    col_name = confirmed.columns[col]
    
    #confirmed cases
    confirmed_day = confirmed[['UID','Province_State','Admin2',col_name]]
    confirmed_day['Date'] = col_name
    confirmed_day['Confirmed'] = confirmed_day[col_name]
    
    #deaths
    deaths_day = deaths[['UID','Province_State','Admin2',col_name]]
    deaths_day['Date'] = col_name
    deaths_day['Deaths'] = deaths_day[col_name]
    
    day = confirmed_day.merge(deaths_day[['UID','Deaths']], on='UID')
    
    #append the records to the output df
    data_out = data_out.append(day[['UID','Province_State','Admin2','Date','Confirmed','Deaths']],ignore_index=True)
    
    #increment day
    col = col + 1
    
#write the output file
url = 'C:\\Users\\' + getpass.getuser() + '\\Documents\\GitHub\\\covid-19\\data\\covid_data.csv'
data_out.to_csv(url)

