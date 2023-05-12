import pandas as pd
import numpy as np
import mysql.connector as sql
import haversine as hs
import gmplot
from haversine import Unit
from flask import Flask, request, render_template
from numpy import empty
import requests
address = "toronto" 


app = Flask(__name__)

# Making a database connection
db_connection = sql.connect(host="localhost",
  user="Divya",
  password="Divya23@",
  database="ontario_firehydrants")

db_cursor = db_connection.cursor()

# Reading from table: "FireHydrants_locations"
db_cursor.execute('select * from FireHydrants_locations')

hydrant_locations = db_cursor.fetchall()

df_hydrant_locations = pd.DataFrame(hydrant_locations)
df_hydrant_locations.columns = ['id',
 'latitude',
 'longitude',
 'geometry',
 'facility_id',
 'location_desc',
 'city_id',
 'status',
 'created_at']


@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    key = "AIzaSyCPy6stcEvj-DujE12plVZ0-qbfdcWbJ1E"
    text = request.form['text']

    is_non_empty= bool(text)

    print(is_non_empty)
    if is_non_empty == False:
      processed_text = "toronto"
    else:
      
      processed_text = text

    url = ("https://maps.googleapis.com/maps/api/geocode/json?address=" + processed_text + "&key=" + key)
    response = requests.get(url)
    resp_json_payload = response.json()

    lat = resp_json_payload['results'][0]['geometry']['location']['lat']
    long = resp_json_payload['results'][0]['geometry']['location']['lng']


    ##                                          DEFINING DISTANCE FUNCTION AND FETCHING NEAREST 5 FIRE HYDRANTS FUNCTION

    ## Haversine Distance can be defined as the angular distance between two locations on the Earth’s surface.
    ## Method to find distance between two coordinates

    def find_distance(given_latitude,given_longitude,df_lat,df_long): 
      dist=hs.haversine((given_latitude,given_longitude),(df_lat,df_long),unit=Unit.METERS)
      return round(dist,2)


    ## Method to fetch 5 nearest hydrants

    def find_nearest(given_latitude, given_longitude):
      distances = df_hydrant_locations.apply(
          lambda row: find_distance(given_latitude,given_longitude,row['latitude'],row['longitude']), 
          axis=1)
      five_nearest = distances.nsmallest(5, keep='all')
      return five_nearest

    nearest_hydrants = find_nearest(lat, long)
    hydrants_loc =  np.array([lat, long])

    #print("Latitude         Longitude         Distance")
    for index, value in nearest_hydrants.items():
      loc_lat = df_hydrant_locations.loc[index]['latitude']
      loc_lng = df_hydrant_locations.loc[index]['longitude']
      hydrants_loc = np.append(hydrants_loc,[float(loc_lat),float(loc_lng)], axis =0 )

    reshaped1 = hydrants_loc.reshape((6,2))
    reshaped = reshaped1.tolist() 
    print(reshaped1)
    #return processed_text
    list_object = [lat, long]
    return render_template("index.html", list_to_send=list_object, render_data =reshaped )


  

if __name__=="__main__":
	app.run()