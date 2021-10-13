from flask import Flask
from flask import jsonify
from flask import request
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
def get_all_stars():
  output = []
  for s in series_collection.find():
    output.append({'name' : s['name'], 'year' : s['year']})
  return jsonify({'result' : output})

@app.route('/series/<int:year>', methods=['GET'])
def get_one_series(year):
  output = []
  s = series_collection.find_one({'year' : year})
  if s:
    output.append({'name' : s['name'], 'year' : s['year']})
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/series/name=<name>|year=<int:year>', methods=['POST'])
def add_series(name,year):
  output = []
  s=series_collection.insert_one({"name": name, "year": year})
  for s in series_collection.find():
    output.append({'name' : s['name'], 'year' : s['year']})
  return jsonify({'result' : output})

@app.route('/series/name=<name>|year=<int:year>', methods=['DELETE'])
def delete_series(name,year):
  output = []
  query = {'name': name, 'year': year}
  s=series_collection.delete_one(query)
  for s in series_collection.find():
    output.append({'name' : s['name'], 'year' : s['year']})
  return jsonify({'result' : output})

@app.route('/series/year=<int:year>', methods=['DELETE'])
def delete_by_year(year):
  output = []
  query = {'year': year}
  s=series_collection.delete_many(query)
  for s in series_collection.find():
    output.append({'name' : s['name'], 'year' : s['year']})
  return jsonify({'result' : output})
