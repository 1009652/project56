import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import keyboard
#import libraries to decode ais data
import socket
import json
from pyais import decode_msg
from pyais import exceptions
from pyais.stream import UDPStream
from threading import Thread
import traceback
import time
import geopandas as gpd
import contextily as cx
import xyzservices.providers as xyz
fig, ax = plt.subplots(figsize=(8,8))
extent = (-12600000, -10300000, 1800000, 3800000)
ax.axis(extent)
fig, ax = plt.subplots(figsize=(8, 8))
cx.add_basemap(ax, zoom=1,source=xyz.OpenStreetMap.Mapnik)
plt.show()
# thread.start()