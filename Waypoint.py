# calculates distance between points cumilatively
def Distance(starting_point,ending_point):
    distance    = 0; 
    for j in range(starting_point+1,ending_point):
        easting1,northing1,zone1,hemi1 = latlong2utm(lat[j-1],long[j-1]);
        easting2,northing2,zone2,hemi2 = latlong2utm(lat[j],long[j]);
        distance = distance + math.sqrt(math.pow((easting1-easting2),2) + math.pow((northing1-northing2),2));
#    Adding distance between  last waypoint and home location
    easting1,northing1,zone1,hemi1 = latlong2utm(lat[starting_point],long[starting_point]);
    easting2,northing2,zone2,hemi2 = latlong2utm(lat[ending_point-1],long[ending_point-1]);
    distance = distance + math.sqrt(math.pow((easting1-easting2),2) + math.pow((northing1-northing2),2));
    return distance 
 
# Saving data in waypoint format   
def save_data(dataframe,name,location):
    directory = os.path.dirname(location) + "/generated/";
    define_dir(directory);
    dataframe.to_csv( directory + str(name) + '.waypoints',sep="\t",header=False)

# Creating directory if doesn't exist
def define_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory);
   
# Converting geographic to projected coordinate system   
def latlong2utm(lat,long):
    coord = utm.from_latlon(lat, long);
    easting =  coord[0];
    northing = coord[1];
    zone = coord[2];
    hemi = coord[3];
    return easting,northing,zone,hemi

# For converting projected to geographic coordinate system
def xy2latlong(easting,northing,zone,hemi):
    lat,long = utm.to_latlon(easting,northing,zone,hemi);
    return lat,long

# Imporing necessary libraries
import math
import pandas as pd
import utm
import os 

# Input wayoint file
location = "/home/indshine-2/Downloads/NCL pilot/combined.waypoints";

# Total distance including return to home distance
max_diatance = 8000;

# Reading waypoint file
total_way = pd.read_table(location,header=None)
lat = total_way[8];
long = total_way[9];

# Starting point is 0
starting_point = 0;

# For naming conventions
name = 0;

# Looping over all dataset
for i in range(1,len(lat)):
    distance = Distance(starting_point,i);
    if distance > max_diatance: # Distance is greater than 10,000
        data_frame = total_way[starting_point:i];
        save_data(data_frame,name,location);
        name = name +1;
        starting_point = i;
