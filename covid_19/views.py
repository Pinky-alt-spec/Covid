from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np

df3=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
def indexPage(request):
    confirmedGlobal = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    totalCount=confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData = barPlotData.reset_index()
    barPlotData.columns = ['Country/Region', 'values']
    barPlotData = barPlotData.sort_values(by='values', ascending=False)
    barPlotVals = barPlotData['values'].values.tolist()
    countryNames = barPlotData['Country/Region'].values.tolist()
    dataForMap=mapDataCal(barPlotData, countryNames)
    showMap = 'True'
    context={'totalCount': totalCount, 'barPlotVals': barPlotVals, 'countryNames': countryNames, 'dataForMap': dataForMap, 'showMap': showMap}
    return render(request, 'covid_19/index.html', context)

def mapDataCal(barPlotData, countryNames):
    dataForMap=[]
    for i in countryNames:
        try:
            tempdf = df3[df3['name'] == i]
            temp = {}
            temp["code3"] = list(tempdf['code3'].values)[0]
            temp["name"] = i
            temp["value"] = barPlotData[barPlotData['Country/Region'] == i]['values'].sum()
            temp["code"] = list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    return dataForMap


def indCountryData(request):
    countryNameSe=request.POST.get('countryNames')
    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    totalCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData = barPlotData.reset_index()
    barPlotData.columns = ['Country/Region', 'values']
    barPlotData = barPlotData.sort_values(by='values', ascending=False)
    barPlotVals = barPlotData['values'].values.tolist()
    countryNames = barPlotData['Country/Region'].values.tolist()
    showMap='False'

    countryDataSpe = pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region'] ==countryNameSe][confirmedGlobal.columns[4:-1]].sum()).reset_index()
    countryDataSpe.columns = ['country', 'values']
    countryDataSpe['lagVal'] = countryDataSpe['values'].shift(1).fillna(0)
    countryDataSpe['incrementVal'] = countryDataSpe['values'] - countryDataSpe['lagVal']
    countryDataSpe['rollingMean'] = countryDataSpe['incrementVal'].rolling(window=4).mean()
    countryDataSpe = countryDataSpe.fillna(0)
    datasetsForLine = [
        {'yAxisID': 'y-axis-1','label': 'Daily Cumulated Data', 'data': countryDataSpe['values'].values.tolist(), 'borderColor': '#bf8c00',
         'backgroundColor': '#bf8c00', 'fill': 'false'},
        {'yAxisID': 'y-axis-2','label': 'Rolling Mean 4 days', 'data': countryDataSpe['rollingMean'].values.tolist(),
         'borderColor': '#7d1850', 'backgroundColor': '#7d1850', 'fill': 'false'}]
    axisvalues=countryDataSpe.index.tolist()
    context = {'countryName': countryNameSe, 'axisvalues':axisvalues, 'totalCount': totalCount, 'barPlotVals': barPlotVals, 'countryNames': countryNames, 'showMap': showMap, 'datasetsForLine': datasetsForLine}
    return render(request, 'covid_19/index.html', context)

