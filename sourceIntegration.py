import pandas as pd
import numpy as np
import plotly.express as plot

url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv";
johnHopkinsDataset = pd.read_csv(url)

oxfordDataset = pd.read_csv("owid-covid-data.csv")

URL_DATASET = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
kaggleDataset = pd.read_csv(URL_DATASET)

#johnHopkins has dailyCases the x axis is the dates and the y axis is the countries
#OxfordDataset holds a bunch of other extra info about each country, we can split the first dataset by these variables
#kaggleDataset holds country, confirmed recovered and Deaths for a bunch of dates

print("shape of JH dataset:", johnHopkinsDataset.shape)
print("shape of Oxford dataset:", oxfordDataset.shape)
print("shape of kaggle dataset:", kaggleDataset.shape)

#build list of countries in all datasets
#oxford Countries
oxfordCountries = []
lastCountry = ""
for country in oxfordDataset["location"]:
    workingCountry = str(country).lower()
    if workingCountry != lastCountry:
        lastCountry = workingCountry
        oxfordCountries.append(workingCountry)

#John hopkins countries
JHCountries = []
lastCountry = ""
for country in johnHopkinsDataset["Country/Region"]:
    workingCountry = str(country).lower()
    if workingCountry != lastCountry:
        lastCountry = workingCountry
        JHCountries.append(workingCountry)

JHProvinces = []
lastCountry = ""
for country in johnHopkinsDataset["Province/State"]:
    workingCountry = str(country).lower()
    if workingCountry != lastCountry:
        lastCountry = workingCountry
        JHProvinces.append(workingCountry)

#kaggle countries
kaggleCountries = []
lastCountry = ""
for country in kaggleDataset["Country"]:
    workingCountry = str(country).lower()
    if workingCountry != lastCountry:
        lastCountry = workingCountry
        kaggleCountries.append(workingCountry)

#finding the countries that are in all 3 databases
JHUnifiedCountries = []
unifiedCountries = []
for JHCountry in JHCountries:
    if JHCountry in oxfordCountries:
        if JHCountry in kaggleCountries:
            unifiedCountries.append(JHCountry)
            JHUnifiedCountries.append(JHCountries)

JHunifiedProvinces= []
for JHCountry in JHProvinces:
    if JHCountry not in unifiedCountries:
        if JHCountry in oxfordCountries:
            if JHCountry in kaggleCountries:
                unifiedCountries.append(JHCountry)
                JHunifiedProvinces.append(JHCountry)

unifiedCountries.append("us")


print("count of JH countries: ", len(JHCountries))
print("count of Oxford countries: ", len(oxfordCountries))
print("count of Kaggle countries: ", len(kaggleCountries))
print("count of countries in all 3 datasets: ", len(unifiedCountries))

#drop all countries that aren't present in everydataset
#oxford
dropList = []
for index in oxfordDataset.index:
    if str(oxfordDataset["location"][index]).lower() not in unifiedCountries:
        dropList.append(index)
oxfordDataset = oxfordDataset.drop(dropList)

#John hopkins
dropList = []
for index in johnHopkinsDataset.index:
    if str(johnHopkinsDataset["Province/State"][index]).lower() not in unifiedCountries:
        if str(johnHopkinsDataset["Country/Region"][index]).lower() not in unifiedCountries:
            dropList.append(index)
johnHopkinsDataset = johnHopkinsDataset.drop(dropList)

#kaggle
dropList = []
for index in kaggleDataset.index:
    if str(kaggleDataset["Country"][index]).lower() not in unifiedCountries:
        dropList.append(index)
kaggleDataset = kaggleDataset.drop(dropList)

print("New Oxford dataset shape:", oxfordDataset.shape)
print("New John Hopkins dataset shape:", johnHopkinsDataset.shape)
print("New kaggle dataset shape:", kaggleDataset.shape)

print("Dropping Dates not in kaggle and john hopkins")
#imports for date comparison
from helperFunctions import compare_dates, convert_date

#find dates that are in both john hopkins and kaggle datasets
#commonDates in john hopkins Format
commonDates = []
variableCtr = 0
for variable in johnHopkinsDataset:
    #skip state country, lat, long
    if variableCtr >= 4:
        for index in kaggleDataset.index:
            if compare_dates(kaggleDataset["Date"][index], variable):
                commonDates.append(variable)
                break
    variableCtr += 1

#dropDates from kaggle
dropList = []
for index in kaggleDataset.index:
    if convert_date(kaggleDataset["Date"][index]) not in commonDates:
        dropList.append(index)
kaggleDataset = kaggleDataset.drop(dropList)

#dropDates from johnHopkins
dropList = []
variableCtr = 0
for variable in johnHopkinsDataset:
    #skip state country, lat, long
    if variableCtr >= 4:
        if variable not in commonDates:
            dropList.append(variable)
    variableCtr += 1

johnHopkinsDataset = johnHopkinsDataset.drop(labels=dropList, axis=1)

print("new kaggle shape: ", kaggleDataset.shape)
print("new johnhopkins shape: ", johnHopkinsDataset.shape)

kaggleHopkinsDataset = kaggleDataset
print("Starting comparison")
differentCtr = 0 
totalCtr = 0
for index in kaggleDataset.index:
    kaggleCountry = kaggleDataset["Country"][index]
    JHCountry = johnHopkinsDataset.loc[johnHopkinsDataset["Country/Region"] == kaggleCountry] 
    date = convert_date(kaggleDataset["Date"][index])

    sumOfCases = 0
    differentFlag = False
    for JHindex in JHCountry.index:
        sumOfCases += johnHopkinsDataset[date][JHindex]
        if johnHopkinsDataset[date][JHindex] != kaggleDataset["Confirmed"][index]:
            differentFlag = True
            differentCtr += 1
        totalCtr += 1
    
    if sumOfCases != kaggleDataset["Confirmed"][index]:
        kaggleHopkinsDataset.at[index, "Confirmed"] = sumOfCases

print("Dropping items that arent on the world graph!")
dropList = ["Laos"]
dropNumberList = []
for index in kaggleHopkinsDataset.index:
    if kaggleHopkinsDataset["Country"][index] in dropList:
        dropNumberList.append(index)
print("finished Dropping")
kaggleHopkinsDataset = kaggleHopkinsDataset.drop(dropNumberList)

print("adding iso alpha to dataframe")
import pycountry
import plotly.express as px
# print(df1.head) # Uncomment to see what the dataframe is like
# ----------- Step 2 ------------
list_countries = kaggleHopkinsDataset['Country'].unique().tolist()
# print(list_countries) # Uncomment to see list of countries
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    country_data = pycountry.countries.search_fuzzy(country)
    # country_data is a list of objects of class pycountry.db.Country
    # The first item  ie at index 0 of list is best fit
    # object of class Country have an alpha_3 attribute
    country_code = country_data[0].alpha_3
    d_country_code.update({country: country_code})

    # create a new column iso_alpha in the df
    # and fill it with appropriate iso 3 code
    for k, v in d_country_code.items():
        kaggleHopkinsDataset.loc[(kaggleHopkinsDataset.Country == k), 'iso_alpha'] = v

print("Creating Change in confirmed")
deltaConfirmed = []
workingCountry = ""
countryCtr = 0
workingChange = 0
for index in kaggleHopkinsDataset.index:
    if workingCountry == kaggleHopkinsDataset["Country"][index]:
        if countryCtr > 0:
            workingChange = kaggleHopkinsDataset["Confirmed"][index] - kaggleHopkinsDataset["Confirmed"][index - 1]
    else:
        print("completed: ", workingCountry)
        workingCountry = kaggleHopkinsDataset["Country"][index]
        countryCtr = 0
        
    deltaConfirmed.append(workingChange)
    countryCtr += 1
    workingChange = 0

kaggleHopkinsDataset["DeltaConfirmed"] = deltaConfirmed

kaggleHopkinsDataset.to_csv('sourceIntegration.csv')
