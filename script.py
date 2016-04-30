from flask_restful import Api, Resource
from flask import Flask, jsonify, url_for, redirect, request,render_template
from pymongo import MongoClient
import flask
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = '8a925ea270e30564c2ae01a1fe7115ecd869452cfd18ec2a'
client = MongoClient("mongodb://localhost:27017")
db = client.simple


@app.route('/index/')
def index_show():
     return render_template('index.html')
     
     
@app.route('/index/', methods = ['POST'])
def index_register():
   if request.form['submit'] == 'Accept':
       uid = request.form['user_id']
       comp = request.form['company']
       name = request.form['name']
       address = request.form['address']
       number = request.form['number']
       
       db.card.insert({'uid': uid,
                       'company' : comp,   
                       'name': name , 
                       'address' : address,
                       'number': number})
   return 'Success'     

@app.route('/search/')
def search_show():
     return render_template('search.html')


@app.route('/search/', methods = ['POST'])
def search_print():
     if request.form['submit'] == 'Accept':
       search = request.form['search']
       output = db.card.find({"$or":[{"name" :{'$regex': search }},
                                              {"address" : {'$regex': search}}, 
                                              {"company" : {'$regex': search}}]})
     
     
     return render_template('search.html',output = output)
     
     
@app.route('/delete/', methods = ['GET'])

def cart_addition():
    obj = flask.request.args.get('objectid')
    obj = ObjectId(obj)
    db.card.remove({'_id': obj})
    
    return 'Success'


@app.route('/update/')
def update_show():
     return render_template('update.html')


@app.route('/update/', methods = ['GET','POST'])
def update_print():
       obj = flask.request.args.get('objectid')
       obj =   ObjectId(obj)
       address = request.form['update']
       update = db.card.update({"_id": obj},{ "$set" : { "address": address }}) 
       return 'Success'
   
APP_URL = "http://localhost:8000"
class card(Resource):
    def get(self,name = None):
        data = []
        cursor = db.card.find({"name": name},{"_id":0})
        for a in cursor:
           
            data.append(a)

        return jsonify({"name": name, "response": data})
api = Api(app)        
api.add_resource(card, "/api/<string:name>", endpoint="name")
if __name__ == '__main__':
    app.debug = True
  
    #app.SERVER_NAME = 'localhost'
    #app.SESSION_COOKIE_DOMAIN = 'localhost'
    app.run(host='0.0.0.0', port=8000)