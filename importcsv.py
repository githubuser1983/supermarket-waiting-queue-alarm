#!/usr/bin/env python
import csv
import psycopg2
import uuid
from datetime import datetime

def importall():
    conn = psycopg2.connect(host="postgres",database="supermarket", user="supermarket", password="develop")
    cur = conn.cursor()

    cur.execute("TRUNCATE supermarkets_warn,supermarkets_supermarket,supermarkets_city;")

    with open('csvs/ww-german-postal-codes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile , delimiter=';')
        for row in reader:
           print(row['zipcode']+row['city'])
           cur.execute( "Insert into supermarkets_city (id,postcode,name) values (%s,%s,%s)",(str(uuid.uuid4()),int(row['zipcode']),row['city']))
    with open('csvs/supermarkets_all.csv', newline='', encoding='latin-1') as csvfile:            
        reader = csv.DictReader(csvfile , delimiter=';')
        for row in reader:
            if is_number(row['plz']):
                print(row['plz']+row['adresse'])
                cur.execute( "Insert into supermarkets_supermarket (id,timestamp,address,name,city_id) values (%s,%s,%s,%s,(select id from supermarkets_city where postcode = %s limit 1))",(str(uuid.uuid4()),datetime.now(),row['adresse'],row['supermarkt'],int(row['plz'])))
    cur.close()
    conn.close()

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False       


importall()

