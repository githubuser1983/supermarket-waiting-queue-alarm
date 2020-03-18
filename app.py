from flask import Flask, Response, render_template, request
import json,csv,logging
from wtforms import TextField, Form
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

cities = []

#print(cities)

#with open("ww-german-postal-codes.csv","r") as f:
#    for line in f:
#        cities.append(line.split(";")[1])

cities = ["65549"]

supermaerkte = ["Aldi Werkstatt","Aldi Industriestraße Diez","Lidl Industriestraße Diez","Penny Holzheimerstraße","Penny Innenstadt","Kaufland","Globus",
          "SB-Markt","Tegut Werkstatt","Rewe Richtung Diez","Edeka Linter","Edeka Blumenrod"]

scounter = dict(zip(supermaerkte,len(supermaerkte)*[0]))





class SearchForm(Form):
    autocomp = TextField('Bitte Postleitzahl angeben', id='city_autocomplete')



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


@app.route('/increasecounter', methods=['POST'])
def increase_counter():
    decat = request.form['myCounter']
    print(decat)
    ll = list(zip(scounter.keys(),scounter.values()))
    print(json.dumps(ll))
    return Response(json.dumps(ll),mimetype="application/json")


@app.route('/receivedata', methods=['POST'])
def receive_data():
    decat = request.form['myData']
    print(decat)
    ll = list(zip(scounter.keys(),scounter.values()))
    #print(json.dumps(scounter))
    return Response(json.dumps(ll),mimetype="application/json")

if __name__ == '__main__':
    logging.basicConfig(filename="log.txt",level=logging.INFO)
    app.run(host='192.168.178.20',port=5000)
