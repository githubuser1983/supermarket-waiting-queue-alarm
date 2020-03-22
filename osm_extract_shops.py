# WirVsVirsuHackathon 2020
# Description of the project:
# https://devpost.com/software/supermarket-alarm
# 
# Enhances CSV list into an address list of supermarkets sorted by postcode
# 
# (c) Manuel Neumann
#
from OSMPythonTools.data import Data, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim

import csv, sys

def readCSVFile(filename):
    # Read csv file in the following format:
    # primary_key;zipcode;city;state;community;latitude;longitude
    # return the postcodes as array
    plz = []

    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=';')
        for row in csvReader:
            if row[1].isnumeric() and row[1] not in plz:
                plz.append(row[1])

    return plz

overpass = Overpass()
nominatim = Nominatim()
fileName = sys.argv[1] # Get filename from command line

fileNameToSave = fileName[0:len(fileName) - 4] + '-supermarkets.csv'

plzList = readCSVFile(fileName)
plzList = sorted(plzList)
fieldnames = ['postcode', 'name', 'street']
writer = csv.DictWriter(open(fileNameToSave, "w"), fieldnames=fieldnames, delimiter  =';')
    
# loop over postcodes and get list of supermarkets
 
plzIdx = 0 
for plz in plzList:
    plzIdx += 1
    if plzIdx % 100 == 0:
        print(plzIdx,'/',len(plzList))
    areaId = nominatim.query(plz).areaId()
    if areaId is None:
        continue
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"shop"="supermarket"', includeGeometry=True, out='body')
    result = overpass.query(query, timeout=60)
    
    if result.countElements() <= 0:
            continue
    for item in result.elements():
        if item is None:
            continue
        if item.tag('addr:street') == None or item.tag('addr:postcode') == None or item.tag('name') == None:
            continue
        #add row to output
        writer.writerow({'postcode': str(item.tag('addr:postcode')), 'name': item.tag('name') ,'street': str(item.tag('addr:street'))+' '+str(item.tag('addr:housenumber'))})
    


