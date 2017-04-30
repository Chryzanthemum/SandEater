# # LIBRARIES AND FUNCTIONS

#required libraries
import requests
import json
import time
import math
import pandas as pd
import numpy as np
#custom, do not pip3 install, use from Github
import netcat
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
# Import the MCP4725 module.
# Requires separate installation instructions, see appendix
import Adafruit_MCP4725

def get_mac():
    import uuid
    return str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()

def normalize(a, b):
    return norm([a,b])

def dotproduct(a, b):
    return dot([a,b], [previous_location[1] - current_location[1], previous_location[0] - current_location[0]])

def get_lat_long_backup():
    dat = {"considerIp": "true",
           "radioType": "lte",
           "carrier": "Verizon"
    }
    request = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBih4uDFjhaZKmERCQ61IfqD__mR9RKtuM', json.dumps(dat))
    return json.loads(request.text)

def get_lat_long():
    nc = Netcat('127.0.0.1', 20175)
    lat = str(nc.read_until('$GPVTG'))
    lng = lat
    lat = lat[(lat.find('A,')+2):lat.find(",N")]
    lat = lat[(lat.find(',')+1):]
    lat1 = float(lat[0:2])
    lat2 = float(lat[2:])/60
    lng = lng[(lng.find('N,')+3):lng.find(",W")]
    lng1 = float(lng[0:2])*-1
    lng2 = float(lng[2:])/60
    return(lat2, lng2)

#this one does latitude
def convertlat(z):
    test = math.floor(z/distancelong - 0.01)
    if test == 0:
        return latmaxmin[1]
    else:
        return (test/distancelat)*dlat + latmaxmin[1]


#THIS ONE IS LONGITUDE. LONGITUDE IS X AXIS
def convertlong(z):
    a = z%distancelong
    if a == 0:
        return longmaxmin[0]
    else:
        return (a/distancelong)*dlon + longmaxmin[1]


def go_straight(x):
    dac1.set_voltage(4096, True)
    dac2.set_voltage(4096, True)
    time.sleep(x)


def turn_left(distance, angle):
    #this doesn't exist because we have no test data on the relationship between power on each wheel and how much the frame turns
    #howver if it did exist, I imagine it'd look something like me setting the power of the slower motor to 50%, and graphing a
    #relationship between voltage on the other motor and distance traveled/new angle of turning, the using a python linear solver
    #to find the voltage output/4096
    dac1.set_voltage(2048, True)
    dac2.set_voltage(4096, True)
    time.sleep(.2)
    return a, b

def turn_right(distance, angle):
    #this doesn't exist because we have no test data on the relationship between power on each wheel and how much the frame turns
    #howver if it did exist, I imagine it'd look something like me setting the power of the slower motor to 50%, and graphing a
    #relationship between voltage on the other motor and distance traveled/new angle of turning, the using a python linear solver
    #to find the voltage output/4096
    dac1.set_voltage(4096, True)
    dac2.set_voltage(2048, True)
    time.sleep(.2)
    return a, b

def navigate_brute():
    x = 0
    lat_long = get_lat_long()
    current_location = [lat_long[0], lat_long[1]]
    go_straight(1)
    previous_location = [current_location[0], current_location[1]]
    while x <= df.size()
        previous_location = [current_location[0], current_location[1]]
        lat_long = get_lat_long()
        current_location = [lat_long[0], lat_long[1]]
        target = [df.iloc[x]['Latitude'], df.iloc[x]['Longitude']]
        a = target[0] - current_location[0]
        b = df[1] - current_location[1]
        c = (np.sin(dlat/2))**2 + np.cos(target[0]) * np.cos(current_location[0]) * (np.sin(target[1]/2))**2
        d = 2 * np.arctan2( np.sqrt(c, np.sqrt(1-c) )
        e = 6378.1*1000*d
        if e <= 1
            x = x + 1
        else:
            if d < 90:
                turn_left(e, d)
            else if d > 90:
                turn_right(e, d)
            else if d = 90:
                go_straight()
   print('done')

def navigate_greedy():
    while df['visited'].nunique() >= 1:
        if previous_location == [0,0]:
            current_location = [get_lat_long()['location']['lat'],get_lat_long()['location']['lng']]
        else:
            previous_location = current_location
            current_location = [get_lat_long()['location']['lat'],get_lat_long()['location']['lng']]
        df['dlat'] = df['latitude'] - current_location[0]
        df['dlng'] = df['longitude'] - current_location[1]
        df['a'] = (np.sin(df['dlat']/2))**2 + np.cos(df['latitude']) * np.cos(current_location[0]) * (np.sin(df['dlng']/2))**2
        df['c'] = 2 * np.arctan2( np.sqrt(df['a']), np.sqrt(1-df['a']) )
        df['d'] = 6378.1*1000*df['c']
        print(df['d'])
        df = df[df['d']>=1]
        df['one'] = df.apply(lambda df: normalize(df['dlng'], df['dlat']), axis=1)
        df['fakeindex'] = norm([previous_location[1] - current_location[1], previous_location[0] - current_location[0]])
        df['two'] = df.apply(lambda df: normalize(df['dlng'], df['dlat']), axis=1)
        df['three'] = df['two']/df['one']/df['fakeindex']
        df['degree'] = arccos(clip(df['three'], -1, 1))
        df2 = df[abs(df['degree']) <= 45]
        if df2['a'].count() >= 1:
            #go forward
            go_straight()
        else:
            #get the closest one
            closest = df.idxm['d']
            m = (current_location[0] - previous_location[0])/(current_location[1] - previous_location[1])
            print('current target')
            print(df['visited']['closest'])
            if (current_location[0] - previous_location[0]) >=0:
                if df['latitude'][uh] > m*df['longitude'][closest] + current_location[1]:
                    turn_left()
                else:
                    turn_right()
    print('done')
# # HARD CODED THINGS THAT RUN AT BEGINNING OF CODE

#everything that only runs once
#user defined coordinates
latitude1 = [39.9493562,-75.195382]
latitude2 = [39.94831, -75.195382]
latitude3 = [39.94831, -75.195400]
latitude4 = [39.9493562, -75.195400]
latitudes = [latitude1, latitude2, latitude3, latitude4]
#turn into a list and extract the maximum and minimum
latitudelist = []
longitudelist = []
for latitude in latitudes:
    latitudelist.append(latitude[0])
    longitudelist.append(latitude[1])
latmaxmin = [max(latitudelist), min(latitudelist)]
longmaxmin = [max(longitudelist), min(longitudelist)]
#Create the rectangle that covers the entire area
dlon = longmaxmin[0] - longmaxmin[1]
dlat = latmaxmin[0] - latmaxmin[1]
dlat2 = dlat*(110.54*1000)
dlon2 = abs(dlon*(111.320*1000*math.cos(latmaxmin[0])))

vertices = [[latmaxmin[1],longmaxmin[1]], [latmaxmin[1],longmaxmin[0]], [latmaxmin[0],longmaxmin[0]], [latmaxmin[0],longmaxmin[1]]]
#these are the width and height of the rectangles
distancelat = math.ceil(dlat2)
distancelong = math.ceil(dlon2)
#number of squares
numbersquares = list(range(distancelat*distancelong))
#size of the square
squaresize = 1
current_location = [0,0]
previous_location = [0,0]

# Create 2 DAC instances.
#1 is left, 2 is right
dac1 = Adafruit_MCP4725.MCP4725(busnum = 1)
dac2 = Adafruit_MCP4725.MCP4725(busnum = 2)

#navigate semi-greedy - comment out if running brute force
d = {'fakeindex' : numbersquares, 'longitude' : numbersquares, 'degree' : numbersquares, 'distance' : numbersquares, 'visited' : numbersquares}
df = pd.DataFrame(data=d, index=numbersquares)
#THIS PLUGS IN LAT/LNG COORDINATES FOR EVERY SINGLE SQUARE
df['latitude'] = df['fakeindex'].apply(lambda x: convertlat(x))
df['longitude'] = df['fakeindex'].apply(lambda x: convertlong(x))
navigate_greedy()

#navigate brute force - comment out if running semi-greedy
df = pandas.DataFrame(data = {'Latitude':[latmaxmin[0]], 'Longitude':[longmaxmin[0]]})
x = 0
b = 0
if distancelat >= distancelong:
    while b <= longmaxmin[0]:
        a = latmaxmin[0]
        b = longmaxmin[1] + (x/distancelong)*dlon
        df.append({'Latitude':latmaxmin[0], 'Longitude':b}, ignore_index=True)
        df.append({'Latitude':latmaxmin[1], 'Longitude':b}, ignore_index=True)
        x = x + 1
        b = longmaxmin[1] + (x/distancelong)*dlon
        df.append({'Latitude':latmaxmin[1], 'Longitude':b}, ignore_index=True)
        df.append({'Latitude':latmaxmin[0], 'Longitude':b}, ignore_index=True)
        x = x + 1
else:
    while b <= latmaxmin[0]:
        a = longmaxmin[0]
        b = latmaxmin[1] + (x/distancelat)*dlat
        df.append({'Latitude':b, 'Longitude':longmaxmin[0]}, ignore_index=True)
        df.append({'Latitude':b, 'Longitude':longmaxmin[1]}, ignore_index=True)
        x = x + 1
        b = latmaxmin[1] + (x/distancelat)*dlat
        df.append({'Latitude':b, 'Longitude':longmaxmin[1]}, ignore_index=True)
        df.append({'Latitude':b, 'Longitude':longmaxmin[0]}, ignore_index=True)
        x = x + 1
navigate_brute()
