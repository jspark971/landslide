from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
import pandas as pd
import numpy as np
import folium
import os
import geocoder


store_data = pd.read_csv("global_landslides.csv")
landslide_map = folium.Map(tiles="Stamen Terrain", zoom_start = 6)
store_data = store_data[:1]

app = Flask(__name__)

my_popup_html="""
<!DOCTYPE html>
<html><head>
<style>
table {{ width: 100%;}}
    
    table, th, td {{
      border: 1px solid black;
      border-collapse: collapse;
      }}

    th, td {{
      padding: 5px;
      text-align: left;
  }}
  table#t01 tr:nth-child(odd) {{
      background-color: #8e8;
  }}
  table#t01 tr:nth-child(even) {{
      background-color:#fff;
  }}
  </style>
  </head>
  <body>
    <table id="t01">
      <tr> <td>Country</td> <td>{country}</td> </tr>
      <tr> <td>Location</td> <td>{nearest_places}</td> </tr>
      <tr> <td>date</td> <td>{date}</td></tr>
      <tr> <td>Landslide type</td> <td>{landslide_type}</td></tr>
      <tr> <td>Trigger</td> <td>{trigger}</td> </tr>
      <tr> <td>Fatalities</td> <td>{fatalities}</td> </tr>
      <tr> <td>Landslide size</td> <td>{landslide_size}</td></tr>
      <tr> <td>Latitude</td> <td>{latitude}</td></tr>
      <tr> <td>Longitude</td> <td>{longitude}</td></tr>
    </table>
    
  </body>
  </html>
  """
  
for _, row in store_data.iterrows():
  try:
    tableFrame = folium.IFrame(html = my_popup_html.format(**row),width =500, height = 300)
    popupTable = folium.Popup(tableFrame, max_width= 500)
    folium.CircleMarker(
      location = [row["latitude"], row["longitude"]],
      radius = 5,
      fill_color = "Brown",
      popup  = popupTable
      ).add_to(landslide_map)
  except:
    pass

def shift_map(x,y):
  try:
  	bb = [[x - 10, y-10],[x+10,y+10]]
  except:
    bb = [[-130,30],[-120,40]]
  landslide_map.fit_bounds(bb)
  return landslide_map._repr_html_()

@app.route("/")
def hello():
  #Problem: for some reason it does not make the fun the inin_map()
  #         which is a function that makes the map with the dots
  #         This is the reason why when i first run the program, the map is okay
  #         but when i shift the location, the dots go away
  #         I currently made the first call work by templating the html file made before

  myhtml = open("my_map.html")
  return myhtml.read()
  #replace the code with this after solving the problem.
  #return landslide_map.__repr_html_()

@app.route("/<name>")
def sayhi(name):
	g = geocoder.google(name)
	x,y = g.lat,g.lng

	return shift_map(x,y)

@app.route("/<name>/<location>")
def sayhiatplace(name, location):
  return render_template('layouts.html', name=name, location=location)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host = '0.0.0.0', port = port, debug = True)