# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:46:55 2020

@author: vtfog
"""

import pandas

#parameters
start_day = "1/22/20"
data_out = pandas.DataFrame(columns = ['Province_State','Admin2','Date','Val'])

#get data from git
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
confirmed = pandas.read_csv(url,error_bad_lines=False)

#column range
col = confirmed.columns.get_loc(start_day)
num_cols = len(confirmed.columns)

#testing
#print('Start Col: ' + str(col))
#print('Stop Col: ' + str(num_cols))

while col < num_cols:
    
    #create the daily dataframe slice
    col_name = confirmed.columns[col]
    confirmed_day = confirmed[['Province_State','Admin2',col_name]]
    confirmed_day['Date'] = col_name
    confirmed_day['Val'] = confirmed_day[col_name]
    
    #df = confirmed_day[['Province_State','Admin2','Date','Val']]
    
    #append the records to the output df
    data_out = data_out.append(confirmed_day[['Province_State','Admin2','Date','Val']],ignore_index=True)
    
    #increment day
    col = col + 1
    
#write the output file
url = 'C:\\Users\\534507\\Documents\\GitHub\\covid-19\\data\\confirmed.csv'
confirmed.to_csv(url)

