from flask import Flask
from flask import jsonify
from flask import request
from bson.json_util import dumps
import pymongo
import os

app = Flask(__name__)

# Create the client
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Connect to our database
db = client['SeriesDB']
# Fetch our series collection
series_collection = db['series']

@app.route('/series', methods=['GET'])
def get_one_series_year():
  year=request.args.get('year', default = 1, type = int)
  name=request.args.get('name', default = '*', type = str)
  cast=request.args.get('cast', default = '*', type = str)
  if year != 1:
    return dumps(list(series_collection.find({'year': year})))
  elif name != '*':
    return dumps(list(series_collection.find({'name': name})))
  elif cast != '*':
    return dumps(list(series_collection.find({'cast': cast})))
  else:
    return dumps(list(series_collection.find()))


@app.route('/series', methods=['POST'])
def add_series():
  year=request.args.get('year', default = 1, type = int)
  name=request.args.get('name', default = '*', type = str)
  cast=request.args.get('cast', default = '*', type = str)
  cast=cast.split("|")
  series_collection.insert_one({"name": name, "year": year, "cast": list(cast)})
  return  dumps(list(series_collection.find()))  
  

@app.route('/series', methods=['DELETE'])
def delete_series():
  name=request.args.get('name', default = '*', type = str)
  year=request.args.get('year', default = 1, type = int)
  if name != '*':
    query = {'name': name}
    series_collection.delete_one(query)
  if year != 1:
    query = {'year': year}
    series_collection.delete_one(query)
  return  dumps(list(series_collection.find()))


@app.route('/series', methods=['PATCH'])
def update():
  year=request.args.get('year', default = 1, type = int)
  name=request.args.get('name', default = '*', type = str)
  cast=request.args.get('cast', default = '*', type = str)
  if name != '*' and year != 1:
    myquery = { "name": name }
    newvalues = { "$set": { "name": name, "year": year } }
    series_collection.update_one(myquery, newvalues)
  elif name != '*' and cast != '*':
    cast=cast.split("|")
    myquery = { "name": name }
    newvalues = { "$set": { "name": name, "cast": list(cast) } }
    series_collection.update_one(myquery, newvalues)
  return  dumps(list(series_collection.find()))


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), 
            port=int(os.getenv('PORT', 4444)))
