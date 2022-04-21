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
us_tc.rolling(window=30).mean()['total_cases'].plot()
#plot.show()

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


