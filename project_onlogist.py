from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import folium
from geopy.geocoders import Nominatim
import googlemaps
from datetime import datetime
import csv

# start webdriver
driver = webdriver.Chrome()

time.sleep(1)

# go to login site
driver.get("https://portal.onlogist.com/secure/login")

# find username and password field
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("enter username")
password.send_keys("enter password")

# press login button
password.send_keys(Keys.RETURN)

# wait until the website is loaded
time.sleep(2)

# open the website with the data I wanna scrape
driver.get("https://portal.onlogist.com/orders?__clear=true")

# sort the rides by price
sort = driver.find_element(By.XPATH, '//*[@id="results"]/div[1]/table/thead/tr/th[9]/a')
sort.click()
sort2 = driver.find_element(By.XPATH, '//*[@id="results"]/div[1]/table/thead/tr/th[9]/a')
sort2.click()

# collect all starting locations in a list
start_locations = []
counter_s = 0
start_location_class = driver.find_elements(By.CLASS_NAME, "col3.start_name")
for start_element in start_location_class:
    if counter_s == 0: # skip first object because it is not a location
        counter_s = counter_s + 1
        continue
    start_locations.append(start_element.text.replace("\n", " "))

# collect all destinations in a list
destinations = []
counter_d = 0
destination_class = driver.find_elements(By.CLASS_NAME, "col4.destination_name")
for dest_element in destination_class:
    if counter_d == 0: # skip first object because it is not a location
        counter_d = counter_d + 1
        continue
    destinations.append(dest_element.text.replace("\n", " "))

# using the google api to find the coordinates
# inserting the google drive api key
gmaps = googlemaps.Client(key = "enter google drive api key")

# getting coordinates of the starting address and collect them in a list
# no idea what the [0] does but it doesn work without
start_lats = []
start_longs = []
for start_co_element in start_locations:
    geocode_starting_location = gmaps.geocode(start_co_element)
    lat_start = geocode_starting_location[0]["geometry"]["location"]["lat"]
    start_lats.append(lat_start)
    long_start = geocode_starting_location[0]["geometry"]["location"]["lng"]
    start_longs.append(long_start)

# getting coordinates of the starting address and collect them in a list
dest_lats = []
dest_longs = []
for dest_co_element in destinations:
    geocode_destination = gmaps.geocode(dest_co_element)
    lat_dest = geocode_destination[0]["geometry"]["location"]["lat"]
    dest_lats.append(lat_dest)
    long_dest = geocode_destination[0]["geometry"]["location"]["lng"]
    dest_longs.append(long_dest)

# put lat and long together and collect it in a list in a list for the starting point
start_comco_lat = []
start_comco_long = []
for i in range(len(start_lats)):
    start_comco_lat.append(start_lats[i])
    start_comco_long.append(start_longs[i])
start_coordinates = [list(pair) for pair in zip(start_comco_lat, start_comco_long)] # this for loop will combine lat and lng together in a list in a list zip() will only combine in a tupel

# put lat and long together and collect it in an array for the destination
dest_comco_lat = []
dest_comco_long = []
for j in range(len(dest_lats)):
    dest_comco_lat.append(dest_lats[j])
    dest_comco_long.append(dest_longs[j])
dest_coordinates = [list(pair) for pair in zip(dest_comco_lat, dest_comco_long)]

#define the center of the map
map_center = [48.152778, 11.533333] # rkp, neuhausen
mymap = folium.Map(location = map_center, zoom_start = 5)

# mark location on the map
counter_start = 0
counter_dest = 0
for start_finalcomco_element in start_coordinates:
    folium.Marker(start_finalcomco_element, popup = start_locations[counter_start]).add_to(mymap) # mark them at the coordinates, with address as popup
    counter_start = counter_start + 1
for dest_finalcomco_element in dest_coordinates:
    folium.Marker(dest_finalcomco_element, popup = destinations[counter_dest], icon=folium.Icon(color='black')).add_to(mymap) # mark them at the coordinates, with address as popup
    counter_dest = counter_dest + 1
# add lines between starting point and destinations
for line_index in range(len(start_coordinates)):
    folium.PolyLine([start_coordinates[line_index], dest_coordinates[line_index]], color = "blue", opacity = 1, weight = 2.5).add_to(mymap)

# save the map as an html.file
mymap.save("map_onlogist.html")

# show the map
mymap

# WebDriver beenden

driver.quit()
