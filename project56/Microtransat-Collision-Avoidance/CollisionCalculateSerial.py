import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import keyboard
#import libraries to decode ais data
import serial
import json
from pyais import decode_msg, NMEAMessage
from pyais import exceptions
from pyais.exceptions import InvalidNMEAMessageException as inme
from pyais.exceptions import MissingMultipartMessageException as mmme
import pyais.exceptions as allexceptions
from pyais.stream import UDPStream
from pyais.stream import FileReaderStream
from threading import Thread
import traceback
import time


class formula:
    def __init__(self, x, y ,speed,angle):
        self.angle = angle
        self.speed = speed
        self.x = x
        self.y = y

    def updateAngle(self, angle):           #update the angle of the boat
        self.angle = angle

    def update(self, x, y ,speed):          #update all the values of the boat
        self.speed = speed
        self.x = x
        self.y = y
        
    def calculateNewCoords(self,time):
        # calculate the new coords
        # cos = overstaande-zijde /schuine-zijde
        # schuine zijde is: s = v*t  
        # cos(180 -angle)    dit doen we om er voor te zorgen dat er altijd een driehoek is waar het mogelijk is om de berekening op uit te voeren.
        # dus overstaand is schuine-zijde * cos
        # + oude coordinaten maakt niewe coordinaten
        dY = 0
        dX = 0 
        if(self.angle <= 90):
            dY = (self.speed*time)*np.cos(np.radians(self.angle))         
            dX = (self.speed*time)*np.sin(np.radians(self.angle))
        elif(self.angle <= 180):
            dY = (self.speed*time)*np.cos(np.radians(180 - self.angle))        
            dX = (self.speed*time)*np.sin(np.radians(180 - self.angle))
            dY = dY *-1
        elif(self.angle < 270):
            dY = (self.speed*time)*np.cos(np.radians(self.angle -180))
            dX =(self.speed*time)*np.sin(np.radians(self.angle -180))
            dX = dX *-1
            dY = dY *-1
        elif(self.angle <= 360):
            dY = (self.speed*time)*np.cos(np.radians(360 - self.angle))        
            dX = (self.speed*time)*np.sin(np.radians(360 - self.angle))   
            dX = dX *-1
        self.y = self.y +dY
        self.x = self.x + dX

def DistanceBetweenPoints(x1,y1,x2,y2):                 # pythagoras om afstand tussen 2 punten te berekenen
    return np.sqrt(((x2-x1)**2)+((y2-y1)**2) )

def coordsToMeters(lon,lat):                    # change the values from longitude/ latitude to meters
    try:
        lon = lon.replace(' ','')               # try to remove empty spaces from string
        lat = lat.replace(' ','') 
    except:
        pass
    lon = float(lon)
    lat = float(lat)
    x = 1852 * (60 * (lon - int(lon)))         # calculate the x and y in meters from longitude latitude
    y = 1852 * (60 * (lat - int(lat)))
    return x,y

def knotsToMPS(speed):                          #change the speed to meters per second
    # speed = speed.replace(' ','')                #try to remove empty spaces from string
    speed = float(speed)
    return (speed *1.852)/3.6

def calculatedistances():
    global Formula1
    global own_x
    global own_y
    global listThey_x
    global listThey_y

    Formula1.update(ownx,owny,ownSpeed)                        #update to the new x and y coordinates
    for i in range(0,amountOfCoords,1):                        #calculate the new coordinates
        Formula1.calculateNewCoords(timeInterval)
        own_x.append(Formula1.x)
        own_y.append(Formula1.y)
    for j in range(0, len(listThey_x)):
        for k in range(0, len(listThey_x[j])):
            distance = DistanceBetweenPoints(own_x[k], own_y[k], listThey_x[j][k] ,  listThey_y[j][k])      #calculate the distance between our ship and another ship
            if distance < dangerDistance:           # if the distance is too small update the heading
                own_x = []
                own_y = []
                calculateNewHeading()
    return

def calculateNewHeading():                  # update the heading
    #heading is updated in a specific order. 
    # first add 5 to the origal heading
    # then substract 10 from the new heading
    # then add 15 from the new heading
    # then substract 20 from the new heading
    # this will continue untill a heading has been found, where there will be no collision
    global Formula1
    heading = Formula1.angle
    global h
    if (h % 2) == 0:
        h = h * -1
    heading = heading +h
    h += 5 
    #print(heading)
    if (heading < 0):
        print(heading)
        heading = 360 + heading
    if (heading > 360):
        print(heading)
        heading = heading - 360
    Formula1.updateAngle(heading)
    calculatedistances()

def graph(x1, x2, y1, y2, i,blockBool):
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.xlim(x1-100000, x1+100000)                                  #set the size of the graph
    plt.ylim(y1-100000, y1+100000)
    plt.gca().set_aspect('equal', adjustable='box') 
    plt.text(1, 1, 'frame ' + str(i), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    plt.scatter(x1,y1,c="red",s=700)                               # circle of minimum distance from the ship
    plt.scatter(x1, y1, c="green", label = "Eigen boot")            # display our own ship 

    plt.plot(own_x, own_y, color = "green", label = "Koers eigen boot", linestyle = '--')       #display our heading
    plt.plot(xoud,youd,color="blue", label= "Oude koers eigen boot", linestyle='--')            #display old heading before calculations

    for ship in range(len(x2)):                                             # go trough all the ships and display the ships and the heading
        plt.scatter(x2[ship][i], y2[ship][i], c="red", label = list(ships)[ship])
        plt.plot(x2[ship],y2[ship], color = "red", linestyle = '--')
    plt.title('AIS')    
    mng = plt.get_current_fig_manager()
    
    plt.legend()
    plt.show(block=blockBool)           #decides if the next frame is displayed False is same frame , True is next Frame
    plt.pause(0.00000000001)
    plt.clf()
    # plt.close()
    
def update():

    i = 0
    update = False
    while i < amountOfCoords:
        # originalListOfCoords();
        if keyboard.is_pressed('a'):                               # if the left arrow is pressed go one frame back
            if i == 0:                                                      # prevent list index out of range
                i = 0
            else:
                i -= 1
            graph(own_x[i], listThey_x, own_y[i], listThey_y, i, update) 
        elif keyboard.is_pressed('d'):                            # if the right arrow is pressed go one frame forward
            calculatedistances()
            calculateOtherCoords()
            if i == amountOfCoords-1:                                      # prevent list index out of range
                i = amountOfCoords-1
            else:
                i += 1
            graph(own_x[i], listThey_x, own_y[i], listThey_y, i, update) 
# ip and port for ais
UDP_IP = "127.0.0.1"
UDP_PORT = 10110
ser = serial.Serial("/dev/ttyUSB0",baudrate=9600)
dangerDistance = 10000
own_x = []
own_y = []
they_x = []
they_y = []
listThey_x = []
listThey_y = []
xoud = []
youd = []
h = 0
ownx,owny = coordsToMeters(4.30,54.5)
ownSpeed = 2
Formula1 = formula(ownx, owny,ownSpeed,1)         #onze boot
timeInterval = 350
amountOfCoords = 1000
ships = {}
shipData = []

def getShips():
    #maybeuse udp streamdddddd
    keys = ['mmsi','lon','lat','speed','course','heading']
    decoded_data = []
    # for msg in ser.readline():
    while True:
        msg = ser.readline().decode('utf-8')
        if msg[0] == '!':
            msg = msg.strip('\x00\r\n')
            print(msg)
            # time.sleep(10)
    #        for message in FileReaderStream("/dev/ttyUSB0"):
    #            decoded_msg = message.decode()
            try:
                decoded_msg = decode_msg(msg)   
            except (inme,mmme):
                print("ERROR")
            except mmme:
                print("ERROR")
            except allexceptions:
                print("SOME error")
            # print(decoded_msg)
            print(decoded_msg)
            if decoded_msg['type'] == 5 or decoded_msg['type'] == 8:
                print(f"WRONG AIS TYPE MESSAGE{decoded_msg['type']}")
                # print(decoded_msg.content)
            else:
                try:
                    selected_data = [decoded_msg[key] for key in keys]
                    #if(int(selected_data[5]) != 511):
                    if(1):
                        if selected_data[0] not in ships.keys():
                            print(f"NUMBER OF SHIPS{len(ships)}")
                            shipData.append(selected_data)
                            ships.update(zip([ship[0] for ship in shipData], shipData))
                        elif selected_data[0] in ships.keys() and selected_data != ships[selected_data[0]]:
                            ships[selected_data[0]] = selected_data
                            print(f"DATA CHANGED!{selected_data[0]}")
                            # ship.append(selected_data)
                        # print(f"ships{ships}")
                except KeyError:
                    print("KeyError")
                    print(traceback.format_exc())
                    print(decoded_msg)
        print(ships)


def calculateOtherCoords():
    global listThey_x
    global listThey_y
    global they_x
    global they_y
    listThey_x = []
    listThey_y = []
    # print(f"SHIPS[0]{[ship[0] for ship in ships]}")
    # print(f"SHIPSSS{ships}")
    for i in list(ships.keys()):                             # go through list of all ships from ais data
        x,y = coordsToMeters(ships[i][1], ships[i][2])      #change to meters
        speed = knotsToMPS(ships[i][3])                     # change to meters per second
        angle = ships[i][5]
        # angle = angle.replace(' ','')                       
        angle = int(angle)
        Formula2 = formula(x,y,speed,angle)                 #set all the data in the formula
        for j in range(0,amountOfCoords,1):                 #calculate the new coordinates and put it in a list.
            Formula2.calculateNewCoords(timeInterval)
            they_x.append(Formula2.x)
            they_y.append(Formula2.y)
        listThey_x.append(they_x)                           #list of coordinates list per ship     
        listThey_y.append(they_y)
        # print(f"THEY X COORDINATE: {they_x[5]}")
        # print(f"THEY Y cOORDINGATE: {they_y[5]}")
        they_x = []
        they_y = []
def originalListOfCoords():
    for i in range(0,amountOfCoords,1):                     #calculate the original coordinates of our own ship to display it later       
        Formula1.calculateNewCoords(timeInterval)
        xoud.append(Formula1.x)
        youd.append(Formula1.y)


thread = Thread(target = getShips)

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(1, 1, 1)

thread.start()
time.sleep(1)
## calculateOtherCoords()
originalListOfCoords()
# # calculateOtherCoords()
calculatedistances()
# # calculatedistances()
plt.plot(xoud,youd,color="blue", label= "Oude koers eigen boot", linestyle='--')            #display old heading before calculations
while True:
    update()
