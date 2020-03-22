import sqlite3

# Database
database = "database.db"


database = sqlite3.connect(database)
cursor = database.cursor()

# Restart Database
cursor.execute("drop table supermarkt")
cursor.execute("drop table warnung")
cursor.execute("drop table meldungen")

cursor.execute("CREATE TABLE supermarkt(id INTEGER PRIMARY KEY, name TEXT, plz TEXT, adresse INT)")
cursor.execute("CREATE TABLE warnung(id INTEGER PRIMARY KEY, hash TEXT, dtime DATETIME)")
cursor.execute("CREATE TABLE meldungen(supermarkt_id INT, warnung_id INT, FOREIGN KEY(supermarkt_id) REFERENCES supermarkt(id), FOREIGN KEY(warnung_id) REFERENCES warnung(id))")


with open("supermaerkte.csv","r") as f:
    f.readline()
    for line in f:
        line = line.replace("\n","")
        plz,name,adresse = line.split(";")
        cursor.execute("INSERT INTO supermarkt(plz, name, adresse) VALUES" +
               "('" + str(plz) + "','" + str(name) + "','" + adresse + "');")
database.commit()

result = cursor.execute("select * from supermarkt")
for row in result:
    print(row)