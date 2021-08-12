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

import pymysql
pymysql.install_as_MySQLdb()

"""
conn = pymysql.connect(
    host = 'localhost',
    port = 8080,
    user = 'user',
    passwd = 'user',
    db = 'student'
)
"""

"""
#geht aktuell nicht, bekomme es nicht hin
engine = create_engine('mysql://user:user@localhost:8080/student')
print("test1")
crimes = pd.read_sql_table('Chicago_Crimes_sample', con=engine, chunksize=500)
engine.dispose()
print("test2")
"""


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

crimes['Year'] = crimes['Year'].astype('int')
#in testing we found that there is a faulty line, where the year is specified as 41, this whole line gets deleted,
# because the probability of it beiing a faulty row in general is high and we have enough other entrys
crimes = crimes[crimes.Year != 41]
#currently not needed
#crimes['mmddyyyy'] = crimes['Date'].astype(str).str[0:10].astype(str)
#crimes['mmddyyyy'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))

#data preparation
#the month-information gets read from the Date-column
crimes['month'] = crimes['Date'].astype(str).str[0:2].astype(str)
"""

app = Flask(__name__)

#Indexpage
@app.route("/")
def Index():
    return render_template("index.html")
"""
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


#plots
@app.route('/plotmonthly.png')
def plotmonth_png():
    fig = create_figureMonth()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figureMonth():
    fig, ax = plt.subplots()
    ax = crimes['month'].value_counts().sort_index().plot(kind="bar")
    return fig

@app.route('/plotyearly.png')
def plotyear_png():
    fig = create_figureYear()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figureYear():
    fig, ax = plt.subplots()
    ax = crimes['Year'].value_counts().sort_index().plot(kind="bar")
    return fig

@app.route('/arrests.png')
def arrests_png():
    fig = create_figureArrests()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figureArrests():
    fig, ax = plt.subplots()
    ax = crimes['Arrest'].value_counts().sort_index().plot(kind="pie")
    return fig

@app.route('/domestic.png')
def domestic_png():
    fig = create_figureDomestic()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figureDomestic():
    fig, ax = plt.subplots()
    ax = crimes['Domestic'].value_counts().sort_index().plot(kind="pie")
    return fig

@app.route('/crimetypes.png')
def crimetypes_png():
    fig = create_figureCrimeTypes()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figureCrimeTypes():
    fig, ax = plt.subplots()
    ax = crimes['Primary Type'].value_counts()[crimes['Primary Type'].value_counts()> crimes['Primary Type'].value_counts().quantile(0.50)].plot(kind="bar")
    return fig

@app.route('/districts.png')
def districts_png():
    fig = create_figureDistricts()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figureDistricts():
    fig, ax = plt.subplots()
    ax = crimes['District'].value_counts().sort_index().plot(kind="bar")
    return fig


"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

