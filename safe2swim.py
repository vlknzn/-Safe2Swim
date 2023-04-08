import requests
import geocoder
import json
import array
import collections
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium


# This url may change?? maybe
url = 'https://data.ca.gov/datastore/dump/848d2e3f-2846-449c-90e0-9aaf5c45853e?q=&sort=_id+asc&fields=StationName,StationCode,LastSampleDate,TargetLatitude,TargetLongitude,Datum&filters={}&format=json'
response = requests.get(url, allow_redirects=True)
#save the response json
open('safe2swim.json', 'wb').write(response.content)

#load the file
swimData =open('safe2swim.json')
#convert into json
swimDataJson  = json.load(swimData)
swimData.close()

#if you dont have geocoder : pip  install gecoder
mylocation = geocoder.ip('me')
myLong = mylocation.latlng[1]
myLat = mylocation.latlng[0]


waterMap = folium.Map([myLat,myLong],
                        zoom_start=12,
                        fill_color="RdYlGn_r",
                        fill_opacity=0.8,
                        line_opacity=0.3,
                        nan_fill_color="white",
                        legend_name="Safe Swimming Water Measurement Stations in California",
                        )
#iterate through the dataset to calculate  the distance to me
for measurement in swimDataJson["records"]:
    if(measurement[3]== "NaN" or measurement[4] == "NaN"):
        continue
    folium.Marker(
      location=[measurement[3], measurement[4]],
      popup=measurement[0],
   ).add_to(waterMap)

#save map
waterMap.save("text.html")