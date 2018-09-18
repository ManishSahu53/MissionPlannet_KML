# Imporing necessary libraries
import math
import pandas as pd
import utm
import os
import simplekml
import Tkinter
import Tkconstants
import tkFileDialog
from Tkinter import *
import argparse

# calculates distance between points cumilatively


def Distance(starting_point, ending_point):
    distance = 0
    for j in range(starting_point +1, ending_point):
        easting1, northing1, zone1, hemi1 = latlong2utm(lat[j-1], long[j-1])
        easting2, northing2, zone2, hemi2 = latlong2utm(lat[j], long[j])
        distance = distance + \
            math.sqrt(math.pow((easting1-easting2), 2) +
                      math.pow((northing1-northing2), 2))

#    Adding distance between  last waypoint and home location
    easting_home, northing_home, zone1, hemi1 = latlong2utm(
        lat[starting_point], long[starting_point])
    easting_end, northing_end, zone2, hemi2 = latlong2utm(
        lat[ending_point], long[ending_point])
    distance = distance + \
        math.sqrt(math.pow((easting_home-easting_end), 2) +
                  math.pow((northing_home-northing_end), 2))
    return distance

# Saving data in waypoint format


def save_data(data_frame, name, location):
    folder = os.path.splitext(location)[0]
    directory = os.path.join(os.path.dirname(location), folder)
    check_dir(directory)
    kml = simplekml.Kml()

    for i in range(len(data_frame)):
        lat = data_frame.iat[i, 8]
        long = data_frame.iat[i, 9]
        ele = data_frame.iat[i, 10]
        if lat == 0 or long == 0:
            continue

        pnt = kml.newpoint(coords=[(long, lat, ele)], altitudemode="clampToGround")
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_square.png"
    kml.save(os.path.join(directory, str(name) + '.kml'))


# Creating directory if doesn't exist
def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Converting geographic to projected coordinate system


def latlong2utm(lat, long):
    coord = utm.from_latlon(lat, long)
    easting = coord[0]
    northing = coord[1]
    zone = coord[2]
    hemi = coord[3]
    return easting, northing, zone, hemi

# For converting projected to geographic coordinate system


def xy2latlong(easting, northing, zone, hemi):
    lat, long = utm.to_latlon(easting, northing, zone, hemi)
    return lat, long

parser = argparse.ArgumentParser()
parser.add_argument('-md','--maxdistance', help='Give maximum distance of UAV fligh plan', required=True,  type=int)
parser.add_argument('-sed','--startenddistance', help='Give starting point and ending point distance', required=True,  type=int)

args = parser.parse_args()  

# Input wayoint file
location = tkFileDialog.askopenfilenames(
    initialdir="/", title="Select Waypoint file files", filetypes=(("wp files", "*.waypoints"), ("all files", "*.*")))

location = location[0]
#location = 'Turbhe.waypoints'

# Total distance including return to home distance
#max_distance = 7000
max_distance = args.maxdistance

# Starting and Ending distance
startenddistance = args.startenddistance

# Reading waypoint file
total_way = pd.read_table(location, skiprows=[0], header=None)
lat = total_way[8]
long = total_way[9]

# Starting point is 0
starting_point = 0

# For naming conventions
name = 0

# Looping over all dataset
for i in range(1, len(lat)):
    distance = Distance(starting_point, i)

    if distance > max_distance:  # Distance is greater than 10,000
        data_frame = total_way[starting_point:i-1]
        save_data(data_frame, name, location)
        name = name + 1
        starting_point = i-2
