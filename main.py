
import pandas as pd
import numpy as np
import plotly.express as plot

url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv";
data_raw=pd.read_csv(url)
print(data_raw)


data_raw=data_raw.drop(columns=['Lat','Long','Province/State'])
data_raw=data_raw.groupby(by='Country/Region').aggregate(np.sum).T
data_raw.index.name='Date'
data_raw=data_raw.reset_index()
data_raw=data_raw.melt(id_vars='Date').copy()
data_raw.rename(columns={'value':'Confirmed'},inplace=True)
max_date=data_raw['Date'].max()
data_raw['Date']=pd.to_datetime(data_raw['Date'])
data_raw['Date']=data_raw['Date'].dt.strftime('%m/%d/%Y')
total_confirmed=data_raw['Confirmed'].sum()
max_date=data_raw['Date'].max()
print(max_date)
total_confirmed_df=data_raw[data_raw['Date'] == max_date]
print(total_confirmed_df)


fig =plot.bar(data_raw,x='Country/Region', y='Confirmed')
fig.show()

fig=plot.bar(total_confirmed_df.sort_values('Confirmed',ascending=False).head(30), x='Country/Region', y='Confirmed', text='Confirmed')
fig.show()

fig2=plot.scatter(total_confirmed_df,x='Date',y='Confirmed',color='Country/Region')
fig2.show()




#owid data graphs:

import pylab

import pandas as pd
import matplotlib.pyplot as plot

owid_df=pd.read_csv("owid-covid-data.csv")
owid_df.columns
country_df=owid_df.location.unique()

indexer=owid_df[owid_df['location']=='United States'].index
us_tc=owid_df.loc[indexer,'date':'total_cases']
us_tc=us_tc.dropna()
us_tc.set_index('date',inplace=True)
us_tc.plot(figsize=(12,6))

# Plot a 30 day moving average
#us_tc.rolling(window=30).mean()['total_cases'].plot()
plot.show()

def plot_covid_data(country, col, plot_ma=False, y_max=200):
    # Get indexes for location rows equal to country name
    indexer = owid_df[owid_df['location'] == country].index
    # Get dataframe location and column data for country name
    country_df = owid_df.loc[indexer, 'date':col]
    # Delete NaN values
    country_df = country_df.dropna()
    # Set date as index
    country_df.set_index('date', inplace=True)
    # Remove all columns except for what I want
    country_df.drop(country_df.columns.difference([col]), 1, inplace=True)
    country_df.plot(figsize=(12, 6), ylim=[0, y_max])

    # Plot moving average if requested
    if plot_ma:
        # Plot a 30 day moving average
        country_df.rolling(window=30).mean()[col].plot()
    print(country_df.columns)


# Least restrictive lockdown
plot_covid_data('Sweden', 'new_cases_per_million', True)
#plot.show()

# Most restrictive lockdown measures
plot_covid_data('Bolivia', 'new_cases_per_million', True)
#plot.show()



