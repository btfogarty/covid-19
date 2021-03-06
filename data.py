
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
    

#write the output file (csv)
#url = 'C:\\Users\\' + getpass.getuser() + '\\Documents\\GitHub\\\covid-19\\data\\covid_data.csv'
#data_out.to_csv(url)

#write the output file (json)
#url = 'C:\\Users\\' + getpass.getuser() + '\\Documents\\GitHub\\\covid-19\\data\\covid_data.json'
#data_out.to_json(url, orient = 'records', lines = True, indent = 2)

#aggregate data
data_sum = data_out.groupby(['Province_State','Date'], as_index = False)['Confirmed','Deaths'].sum()
data_sum['Date'] = pandas.to_datetime(data_sum['Date'],dayfirst = False)
data_sum = data_sum.sort_values(['Province_State','Date'], ascending = [True, True])

#USA Summary
data_usa = data_out.groupby(['Date'], as_index = False)['Confirmed','Deaths'].sum()
data_usa['Date'] = pandas.to_datetime(data_usa['Date'],dayfirst = False)
data_usa = data_usa.sort_values(['Date'], ascending = [True])
data_usa['Province_State'] = 'USA'
data_usa = data_usa[['Province_State','Date','Confirmed','Deaths']]

data_sum = data_sum.append(data_usa[['Province_State','Date','Confirmed','Deaths']],ignore_index=True)

#Calculate Daily Changes
data_sum['confirmed_diff'] = data_sum.groupby(['Province_State'])['Confirmed'].diff().fillna(0)
data_sum['deaths_diff'] = data_sum.groupby(['Province_State'])['Deaths'].diff().fillna(0)

#Calculate rolling avgs
data_sum['confirmed_3day'] = round(data_sum.groupby(['Province_State'])['confirmed_diff'].rolling(3).mean().reset_index(level=0, drop=True).fillna(0),3)
data_sum['confirmed_5day'] = round(data_sum.groupby(['Province_State'])['confirmed_diff'].rolling(5).mean().reset_index(level=0, drop=True).fillna(0),3)
data_sum['deaths_3day'] = round(data_sum.groupby(['Province_State'])['deaths_diff'].rolling(3).mean().reset_index(level=0, drop=True).fillna(0),3)
data_sum['deaths_5day'] = round(data_sum.groupby(['Province_State'])['deaths_diff'].rolling(5).mean().reset_index(level=0, drop=True).fillna(0),3)

#url = 'C:\\Users\\' + getpass.getuser() + '\\Documents\\GitHub\\\covid-19\\data\\covid_states_data.json'
#data_sum.to_json(url, orient = 'split', index=False, indent = 2)

#Virginia Data
#data_va = data_sum.loc[data_sum['Province_State'] == 'Virginia']
#url = 'C:\\Users\\' + getpass.getuser() + '\\Documents\\GitHub\\\covid-19\\data\\covid_va_data.json'
#data_va.to_json(url, orient = 'records', indent = 2)
#data_va.to_json(url, orient = 'records',  indent = 2)

states = data_sum['Province_State'].unique()
idx = 0

url = 'C:\\Users\\' + getpass.getuser() + '\\Documents\\GitHub\\btfogarty.github.io\\data\\covid_states_data.json'
file = open(url,'w')
file.write('[\n')
#write custom JSON file
while idx < len(states):
    
    print(states[idx])
    file.write('\t{"state":"' + states[idx] + '",\n')
    file.write('\t\t"report":\n')
    file.write('\t\t\t[\n')
    
    #get state data and sort by date
    state_data = data_sum.loc[data_sum['Province_State'] == states[idx]]
    
    num_rows = 1
    len(state_data.index)
    
    for index, row in state_data.iterrows():
        if num_rows + 1 <= len(state_data.index):
            file.write('\t\t\t\t{"Date":"' + str(row['Date'].strftime('%m/%d/%Y')) + '", "Confirmed":' + str(row['Confirmed']) 
                       + ', "Deaths":' + str(row['Deaths']) + ', "Daily_Confirmed":' + str(row['confirmed_diff']) + ', "Daily_Deaths":' + str(row['deaths_diff']) 
                       + ', "Confirmed_3day":' + str(row['confirmed_3day']) + ', "Confirmed_5day":' + str(row['confirmed_5day'])
                       + ', "Deaths_3day":' + str(row['deaths_3day']) + ', "Deaths_5day":' + str(row['deaths_5day']) 
                       + '},\n')
        else:
            file.write('\t\t\t\t{"Date":"' + str(row['Date'].strftime('%m/%d/%Y')) + '", "Confirmed":' + str(row['Confirmed']) 
                       + ', "Deaths":' + str(row['Deaths']) + ', "Daily_Confirmed":' + str(row['confirmed_diff']) + ', "Daily_Deaths":' + str(row['deaths_diff']) 
                       + ', "Confirmed_3day":' + str(row['confirmed_3day']) + ', "Confirmed_5day":' + str(row['confirmed_5day'])
                       + ', "Deaths_3day":' + str(row['deaths_3day']) + ', "Deaths_5day":' + str(row['deaths_5day']) 
                       + ' }\n')
        num_rows = num_rows + 1
    
    file.write('\t\t\t]\n')
    idx = idx + 1
    
    if idx < len(states):
        file.write('\t},\n')
    else:
        file.write('\t}\n')
    
    
    
file.write("]")
file.close()

