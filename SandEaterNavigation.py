
# coding: utf-8

# # LIBRARIES AND FUNCTIONS

# In[1]:

#required libraries
import requests
import json
import time
import math
import pandas as pd
import numpy as np
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm


# In[2]:

def get_mac():
    import uuid
    return str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()


# In[3]:

def normalize(a, b):
    return norm([a,b])


# In[4]:

def dotproduct(a, b):
    return dot([a,b], [previous_location[1] - current_location[1], previous_location[0] - current_location[0]])


# In[5]:

def get_lat_long():
    dat = {"considerIp": "false",
      "wifiAccessPoints": [{
#currently this is hard coded for Penn's mac address, which is obtained using get_mac. If we're off Penn's campus, we have much larger problems to consider.
      "macAddress": "5C:E0:C5:8C:42:99",
        }]
    }
    request = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBih4uDFjhaZKmERCQ61IfqD__mR9RKtuM', json.dumps(dat))
    return json.loads(request.text)


# In[6]:

#this one does latitude
#LATITUDE IS Y AXIS, STOP FUCKING THIS UP
def convertlat(z):
    test = math.floor(z/distancelong - 0.01)
    if test == 0:
        return latmaxmin[1]
    else:
        return (test/distancelat)*dlat + latmaxmin[1]


# In[7]:

#THIS ONE IS LONGITUDE. LONGITUDE IS X AXIS
def convertlong(z):
    a = z%distancelong
    if a == 0:
        return longmaxmin[0]
    else:
        return (a/distancelong)*dlon + longmaxmin[1]


# In[8]:




# In[9]:

def actually_navigate():
    #FIRST TIME WE RUN IT, WE WILL NOT HAVE A DIRECTIONAL VECTOR YET
    current_location = [0,0]
    previous_location = [0,0]
    d = {'fakeindex' : numbersquares, 'longitude' : numbersquares, 'degree' : numbersquares, 'distance' : numbersquares, 'visited' : numbersquares}
    df = pd.DataFrame(data=d, index=numbersquares)
#THIS PLUGS IN LAT/LNG COORDINATES FOR EVERY SINGLE SQUARE
    df['latitude'] = df['fakeindex'].apply(lambda x: convertlat(x))
    df['longitude'] = df['fakeindex'].apply(lambda x: convertlong(x))
    #THIS IS A TERRIBLE IDEA BUT FUCK MY WORKFLOW UP FAM
    while df['visited'].nunique() >= 1:
        if previous_location == [0,0]:
            current_location = [get_lat_long()['location']['lat'],get_lat_long()['location']['lng'] ]
        else:
            previous_location = current_location
            current_location = [get_lat_long()['location']['lat'],get_lat_long()['location']['lng']
        df['dlat'] = df['latitude'] - current_location[0] 
        df['dlng'] = df['longitude'] - current_location[1] 
        df['a'] = (np.sin(df['dlat']/2))**2 + np.cos(df['latitude']) * np.cos(current_location[0]) * (np.sin(df['dlng']/2))**2 
        df['c'] = 2 * np.arctan2( np.sqrt(df['a']), np.sqrt(1-df['a']) ) 
        df['d'] = 6378.1*1000*df['c']
        df = df[df['d']>=1]
        df['one'] = df.apply(lambda df: normalize(df['dlng'], df['dlat']), axis=1)
        df['fakeindex'] = norm([previous_location[1] - current_location[1], previous_location[0] - current_location[0]])
        df['two'] = df.apply(lambda df: normalize(df['dlng'], df['dlat']), axis=1)
        df['three'] = df['two']/df['one']/df['fakeindex']
        df['degree'] = arccos(clip(df['three'], -1, 1))
        df2 = df[abs(df['degree']) <= 45]
        navigate()
        if df2['a'].count() >= 1:
            print('forward')
        else:
            #get the closest one
            closest = df.idxm['d']
            m = (current_location[0] - previous_location[0])/(current_location[1] - previous_location[1])
            print('current target')
            print(df['visited']['closest'])
            if (current_location[0] - previous_location[0]) >=0:        
                if df['latitude'][uh] > m*df['longitude'][closest] + current_location[1]:
                    print('left')
                else:
                    print('right')
    print('done')


# In[ ]:

#         df['degree'] = arccos(clip(df['kms'], -1, 1))
#         if (df[abs(df['degree']) <= 45].count() >= 1):
#             print('forward')
#         else:
#             #get the closest one
#             uh = df.idxm['d']
#             m = (current_location[0] - previous_location[0])/(current_location[1] - previous_location[1])
#             if (current_location[0] - previous_location[0]) >=0 >= 0:        
#                 if df['latitude'][uh] > m*df['longitude'][uh] + current_location[1]
#                     print('left')
#                 else:
#                     print('right')
#print('done')
#if not all visited, find distance to current for all, find theta from distance vector
#if current distance < squaresize, visited = true
#check all 'visited', if all visited, print 'done'
#so I need last checkin, current checkin, function for distance, function for theta
#if exists abs(theta) < 45, go forward
#else find min(distance)


# # HARD CODED THINGS THAT RUN AT BEGINNING OF CODE

# In[10]:

#THIS IS ALL THE STUFF THAT HAS TO RUN ONCE AND ONLY ONCE
#THESE ARE HARD CODED COORDINATES. THESE ARE ALWAYS SUPPOSED TO BE USER DEFINED.
#DON'T FUCK WITH THESE.
latitude1 = [39.9493562,-75.195382]
latitude2 = [39.94831, -75.195382]
latitude3 = [39.94831, -75.195400]
latitude4 = [39.9493562, -75.195400]
latitudes = [latitude1, latitude2, latitude3, latitude4]
#THIS IS A TERRIBLY DEFINED WAY OF DOING THIS BUT THE IDEA IS THAT AT SOME POINT YOU WILL BE ABLE TO UPLOAD A LIST OF COORDINATES
#AND IT WILL EXTRACT THEM FOR YOU. YES I KNOW RIGHT NOW I ONLY HAVE 4.
latitudelist = []
longitudelist = []
for latitude in latitudes:
    latitudelist.append(latitude[0])
    longitudelist.append(latitude[1])
#FIND THE MAX AND MIN LATITUDE/LONGITUDE. YES I KNOW THAT LONGITUDE MAY BE NEGATIVE.
latmaxmin = [max(latitudelist), min(latitudelist)]
longmaxmin = [max(longitudelist), min(longitudelist)]
#THIS IS A REALLY TRAGIC WAY OF FINDING THE COORDINATES OF A RECTANGLE THAT ABSOLUTELY MUST COVER ALL THE HARD CODED COORDINATES
#THIS ALGORITHM IS SHIT BUT ITS MINE.
dlon = longmaxmin[0] - longmaxmin[1] 
dlat = latmaxmin[0] - latmaxmin[1] 
dlat2 = dlat*(110.54*1000)
dlon2 = abs(dlon*(111.320*1000*math.cos(latmaxmin[0])))

vertices = [[latmaxmin[1],longmaxmin[1]], [latmaxmin[1],longmaxmin[0]], [latmaxmin[0],longmaxmin[0]], [latmaxmin[0],longmaxmin[1]]]
#THIS IS THE LENGTH IN METERS OF THE RECTANGLE
distancelat = math.ceil(dlat2)
distancelong = math.ceil(dlon2)
#WE'RE DIVIDING THE RECTANGLE INTO SQUARES THAT COMPLETELY COVER IT, THIS IS HOW MANY
numbersquares = list(range(distancelat*distancelong))
#THIS IS IN METERS
#THIS IS ALMOST ALWAYS GOING TO BE 1 UNLESS I FUCK WITH IT FOR DEMO PURPOSES
squaresize = 1


# In[11]:

actually_navigate()


# In[ ]:



