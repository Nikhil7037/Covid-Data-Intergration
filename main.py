
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







