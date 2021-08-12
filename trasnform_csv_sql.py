import pandas as pd
from sqlalchemy import create_engine

#jeweilige csv einfügen
data = pd.read_csv(r"Chicago_Crimes_2005_to_2007.csv", error_bad_lines=False)

data=data.fillna("NULL") #ersetzen der nan durch NULL

file1 = open("CRIMES.sql","w") #CRIMES.sql muss im selben file vorhanden sein

def checkernull(row,value):

    if row[value] =="NULL":
        return "NULL"
        
    else:
        return f" '{row[value]}' "



for index,row in data.iterrows():
    #
    file1.write(f"VALUES ({row['ID']}, {checkernull(row,'Case Number')}, {checkernull(row,'Date')}, {checkernull(row,'Block')}, {row['IUCR']}, {checkernull(row,'Primary Type')}, {checkernull(row,'Description')}, {checkernull(row,'Location Description')}, {checkernull(row,'Arrest')}, {checkernull(row,'Domestic')}, {row['Beat']}, {checkernull(row,'District')}, '{row['Ward']}', {checkernull(row,'Community Area')}, {checkernull(row,'FBI Code')}, {row['X Coordinate']}, {row['Y Coordinate']}, {row['Year']}, {checkernull(row,'Updated On')}, {row['Latitude']}, {row['Longitude']}, {checkernull(row,'Location')});\n")
    print(index)


file1.close()