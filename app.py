from flask import Flask, Response, render_template, request,send_from_directory
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
    def __init__(self,id,postcode,adress,name):
        self.id = id
        self.postcode = postcode
        self.adress = adress
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
        self.list_of_warnings = [w for w in self.list_of_warnings if (n-w.dtime).total_seconds() <= seconds]
id = 1
supermarkets = [Supermarket(1,65549,"Musterstr.",supermarket) for supermarket in supermaerkte]
for supermarket in  supermarkets:
    supermarket.id = id
    id +=1
supermarkets_by_id = dict([(supermarkt.id,supermarkt) for supermarkt in supermarkets])
supermarkets_by_postcode = dict([(supermarkt.postcode,supermarkt) for supermarkt in supermarkets])
        

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


@app.route('/warn/<id>', methods=['POST'])
def warn(id):
    print(request)
    print(id)
    hashed = hashlib.md5(("-".join([str(x) for x in request.headers])+request.remote_addr).encode("utf-8")).digest()
    print(hashed)
    dtime = datetime.datetime.now()
    supermarket = supermarkets_by_id[int(id)]
    w = Warn(hashed,dtime)
    supermarket.delete_old_warnings()
    accepted = supermarket.accept_warning(w)
    return Response(json.dumps(accepted),mimetype="application/json")


#@app.route('/receivedata', methods=['POST'])
#def receive_data():
#    plz = request.form['plz']
#    ll = []
#    for key in dict_of_supermarkets.keys():
#        location, Sname = key
#        S = dict_of_supermarkets[key]
#        S.delete_old_warnings()
#        ll.append( (Sname, len(S.list_of_warnings)))         
#    #print(json.dumps(scounter))
#    return Response(json.dumps(ll),mimetype="application/json")

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/receivedata',methods=['GET'])
def receive_data():
    page = int(request.args.get('page'))
    size = int(request.args.get('size'))
    search = request.args.get('search')
    postcode = int(request.args.get('postcode'))
    fromPos = page * size
    toPos = ((page + 1)*size)

    searchSplit = []
    if (search != None) :
        searchSplit = search.lower().split()
    ll = []
    for markt in supermarkets:
        found = True
        searchMarket = (markt.name+markt.adress).lower()
        if len(searchSplit) > 0:
            for searchSplitEntry in searchSplit:
                if not searchMarket.__contains__(searchSplitEntry):
                    found = False

        if (postcode == markt.postcode and found): 
            ll.append({ "id":markt.id , "name":markt.name, "adress":markt.adress,"waiting_queue_last_hour":markt.list_of_warnings.__len__(),"waiting_queue_last_24_hour":markt.list_of_warnings.__len__()})

    if (len(ll) < fromPos or len(ll) == 0):
        return Response(json.dumps([]),mimetype="application/json")
    if (len(ll) < toPos):
        toPos = len(ll)

    return Response(json.dumps(ll[fromPos:toPos]),mimetype="application/json")

if __name__ == '__main__':
    logging.basicConfig(filename="log.txt",level=logging.INFO)
    STAGE = "DEV"
    if STAGE == "DEV":
        app.run(host='0.0.0.0',port=5000)
    else:
        app.run(host="192.168.178.20",port=5000)

