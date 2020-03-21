# WirVsVirsuHackathon 2020
# Enhances CSV list into an address list of supermarkets sorted by postcode
# 
# (c) Manuel Neumann
#
from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim

import csv

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

plzList = readCSVFile('ww-german-postal-codes.csv')
writer = csv.writer(open("postal-codes-supermarkets.csv", "w"), delimiter  =';')
    
# loop over postcodes and get list of supermarkets
 
for plz in plzList:
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
        if item.tag('addr:street') == None:
            continue
        row = item.tag('addr:postcode'), item.tag('addr:street'), item.tag('addr:housenumber'),item.tag('name')
        
        #add row to output
        writer.writerow(row)
    


