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

# Saving data in waypoint format


def save_data(data_frame, location):
    folder = os.path.splitext(location)[0]
    directory = os.path.join(os.path.dirname(location), folder)
#    check_dir(directory)
    kml = simplekml.Kml()

    for i in range(len(data_frame)):
        lat = data_frame.iat[i, 8]
        long = data_frame.iat[i, 9]
        ele = data_frame.iat[i, 10]
        if lat == 0:
            continue
        if long == 0:
            continue

        pnt = kml.newpoint(coords=[(long, lat, ele)], altitudemode="clampToGround")
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_square.png"
    kml.save(os.path.join(directory, folder + '.kml'))


# Creating directory if doesn't exist
def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Input wayoint file
location = tkFileDialog.askopenfilenames(
    initialdir="/", title="Select Waypoint file files", filetypes=(("wp files", "*.waypoints"), ("all files", "*.*")))


for wp_file in location:
    # Reading waypoint file
    total_way = pd.read_table(wp_file, skiprows=[0], header=None)
    lat = total_way[8]
    long = total_way[9]
    
    save_data(total_way, wp_file)
