from flask import Flask, render_template, request

#imports
import pandas as pd
import matplotlib.pyplot as plt
from flask import Response
from matplotlib.figure import Figure
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import sqlalchemy
from sqlalchemy import create_engine
import socket
import pickle

import pymysql
pymysql.install_as_MySQLdb()

#Memcached
from pymemcache.client import base
from pymemcache import serde


#geht aktuell nicht, bekomme es nicht hin
print("test0")
engine = create_engine('mysql+pymysql://root:root@my-app-mysql-service:3306/crimes', connect_args={'connect_timeout':120}, pool_pre_ping=True)		
print("test1")
crimes = pd.read_sql('Chicago_Crimes_sample', con=engine.connect())
engine.dispose()
print("test2")



"""
#currently not necessary
crimes01to04 = pd.read_csv('WebApp/tempdatafolder/Chicago_Crimes_2001_to_2004.csv', error_bad_lines=False)
crimes05to07 = pd.read_csv('WebApp/tempdatafolder/Chicago_Crimes_2001_to_2004.csv', error_bad_lines=False)
crimes08to11 = pd.read_csv('WebApp/tempdatafolder/Chicago_Crimes_2001_to_2004.csv', error_bad_lines=False)
crimes12to17 = pd.read_csv('WebApp/tempdatafolder/Chicago_Crimes_2001_to_2004.csv', error_bad_lines=False)
#the smaller dataframes get concatenated to one big one ... later this happens when streaming data gets added to the data from
# the data lake
crimes_list = [crimes01to04, crimes05to07, crimes08to11, crimes12to17]
crimes = pd.concat(crimes_list)
#data preparation
"""
crimes['YEAR'] = crimes['YEAR'].astype('int')
#in testing we found that there is a faulty line, where the year is specified as 41, this whole line gets deleted,
# because the probability of it beiing a faulty row in general is high and we have enough other entrys
crimes = crimes[crimes.YEAR != 41]
#currently not needed
#crimes['mmddyyyy'] = crimes['Date'].astype(str).str[0:10].astype(str)
#crimes['mmddyyyy'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))

#data preparation
#the month-information gets read from the Date-column
crimes['month'] = crimes['Date'].astype(str).str[0:2].astype(str)

#Setting up the connection to the Memcached-service
client = base.Client((str(socket.gethostbyname('my-memcached-service')), 11211), serde=serde.pickle_serde)

app = Flask(__name__)

#Indexpage
@app.route("/")
def Index():
    return render_template("index.html")
    
#subpages
@app.route("/monthly")
def monthlypage():
    return render_template("monthly.html")

@app.route("/yearly")
def yearlypage():
    return render_template("yearly.html")

@app.route("/arrests")
def arrestspage():
    return render_template("arrests.html")

@app.route("/domestic")
def domesticpage():
    return render_template("domestic.html")

@app.route("/crimetypes")
def crimetypespage():
    return render_template("crimetypes.html")

@app.route("/districts")
def districtspage():
    return render_template("districts.html")

#functions to create plots
def create_figureMonth():
    fig, ax = plt.subplots()
    ax = crimes['month'].value_counts().sort_index().plot(kind="bar")  

    return fig

def create_figureYear():
    fig, ax = plt.subplots()
    #ax = crimes['YEAR'].value_counts().sort_index().plot(kind="bar")
    crime_year = pd.read_sql('Crime_Year', con=engine.connect())
    engine.dispose()
    
    crime_year['YEAR'].value_counts().sort_index().plot(kind="bar")
    
    return fig

def create_figureArrests():
    fig, ax = plt.subplots()
    ax = crimes['Arrest'].value_counts().sort_index().plot(kind="pie")
    return fig

def create_figureDomestic():
    fig, ax = plt.subplots()
    ax = crimes['Domestic'].value_counts().sort_index().plot(kind="pie")
    return fig

def create_figureCrimeTypes():
    fig, ax = plt.subplots()
    """
    ax = crimes['PrimaryType'].value_counts()[crimes['PrimaryType'].value_counts()> crimes['PrimaryType'].value_counts().quantile(0.50)].plot(kind="bar")
    """
    ax = crimes['PrimaryType'].value_counts().plot(kind="bar")
    return fig

def create_figureDistricts():
    fig, ax = plt.subplots()
    ax = crimes['District'].value_counts().sort_index().plot(kind="bar")
    return fig

#get the values that are stored in Memcached
result_figureMonth = client.get('figureMonth_key')
result_figureYear = client.get('figureYear_key')
result_figureArrests = client.get('figureArrests_key')
result_figureDomestic = client.get('figureDomestic_key')
result_figureCrimeTypes = client.get('figureCrimeTypes_key')
result_figureDistricts = client.get('figureDistricts_key')

#if no value is stored in Memcached, run the function to calculate value and then store it in the cache
if result_figureMonth is None:
    result_figureMonth = create_figureMonth()
    print(result_figureMonth)
    client.set('figureMonth_key', result_figureMonth)	

if result_figureYear is None:
    result_figureYear = create_figureYear()
    client.set('figureYear_key', result_figureYear)
    
if result_figureArrests is None:
    result_figureArrests = create_figureArrests()
    client.set('figureArrests_key', result_figureArrests)
    
if result_figureDomestic is None:
    result_figureDomestic = create_figureDomestic()
    client.set('figureDomestic_key', result_figureDomestic)
    
if result_figureCrimeTypes is None:
    result_figureCrimeTypes = create_figureCrimeTypes()
    client.set('figureCrimeTypes_key', result_figureCrimeTypes)
    
if result_figureDistricts is None:
    result_figureDistricts = create_figureDistricts()
    client.set('figureDistricts_key', result_figureDistricts)

#plots
@app.route('/plotmonthly.png')
def plotmonth_png():
    fig = result_figureMonth
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plotyearly.png')
def plotyear_png():
    fig = result_figureYear
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/arrests.png')
def arrests_png():
    fig = result_figureArrests
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/domestic.png')
def domestic_png():
    fig = result_figureDomestic
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/crimetypes.png')
def crimetypes_png():
    fig = result_figureCrimeTypes
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/districts.png')
def districts_png():
    fig = result_figureDistricts
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

