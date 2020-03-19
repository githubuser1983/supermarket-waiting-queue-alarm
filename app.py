from flask import Flask, Response, render_template, request
import json,csv,logging, hashlib,datetime
from wtforms import TextField, Form
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

cities = []

#print(cities)

#with open("ww-german-postal-codes.csv","r") as f:
#    for line in f:
#        cities.append(line.split(";")[1])

cities = ["65549"]

supermaerkte = ["Aldi Werkstadt","Aldi Industriestrasse Diez","Lidl Industriestrasse Diez","Penny Holzheimerstrasse","Penny Innenstadt","Kaufland","Globus",
          "SB-Markt","Tegut Werkstadt","Rewe Richtung Diez","Edeka Linter","Edeka Blumenrod"]


class Supermarket:
    def __init__(self,location,name):
        self.location = location
        self.name = name
        self.list_of_warnings = []

    def accept_warning(self,w,seconds=60*60*3): # eine Warnung in 3 Stunden
        n = datetime.datetime.now()
        old_warnings = [ ww for ww in  self.list_of_warnings if w.hashed == ww.hashed]
        if len(old_warnings)>0:
            m = min([ww.dtime for ww in old_warnings])
            M = max([ww.dtime for ww in old_warnings])
            if (n-M).total_seconds()>seconds:
                self.list_of_warnings.append(w)
                return True
            else:
                return False
        else:
            self.list_of_warnings.append(w)
            return True
        
    
    def delete_old_warnings(self,seconds = 60*60):
        n = datetime.datetime.now()
        print([str(x) for x in self.list_of_warnings])
        self.list_of_warnings = [w for w in self.list_of_warnings if (n-w.dtime).total_seconds() > seconds]

dict_of_supermarkets = dict([ ( ("65549",supermarket), Supermarket("65549",supermarket) ) for supermarket in supermaerkte])
        

class Warn:
    def __init__(self, hashed, dtime):
        self.hashed = hashed
        self.dtime = dtime

    def __str__(self):
        return str(self.hashed)+"_"+str(self.dtime)

class SearchForm(Form):
    autocomp = TextField('Bitte Postleitzahl angeben (65549)', id='city_autocomplete')


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(cities), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.headers)
    logging.info(request.remote_addr)
    logging.info(request.headers)
    form = SearchForm(request.form)
    return render_template("search.html", form=form)


@app.route('/warn', methods=['POST'])
def warn():
    data = request.form
    print(request)
    hashed = hashlib.md5(("-".join([str(x) for x in request.headers])+request.remote_addr).encode("utf-8")).digest()
    print(hashed)
    dtime = datetime.datetime.now()
    location = data["location"]
    supermarket = data["supermarket"]
    w = Warn(hashed,dtime)
    S = dict_of_supermarkets[(location,supermarket)]
    S.delete_old_warnings()
    accepted = S.accept_warning(w)
    dict_of_supermarkets[(location,supermarket)] = S
    return Response(json.dumps(accepted),mimetype="application/json")


@app.route('/receivedata', methods=['POST'])
def receive_data():
    plz = request.form['plz']
    ll = []
    for key in dict_of_supermarkets.keys():
        location, Sname = key
        S = dict_of_supermarkets[key]
        S.delete_old_warnings()
        ll.append( (Sname, len(S.list_of_warnings)))         
    #print(json.dumps(scounter))
    return Response(json.dumps(ll),mimetype="application/json")

if __name__ == '__main__':
    logging.basicConfig(filename="log.txt",level=logging.INFO)
    STAGE = "DEV"
    if STAGE == "DEV":
        app.run(host='0.0.0.0',port=5000)
    else:
        app.run(host="192.168.178.20",port=5000)

