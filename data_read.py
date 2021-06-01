# kütüphanelerin hepsi gerekli değildir.
@author: Selim Altıntaş
"""

import http.client, urllib.request, urllib.parse, urllib.error
import urllib3
import time
import json
import csv
import os
import sys
import io
import folium # pip install folium
from folium import plugins
from folium.plugins import search
from folium.plugins import MiniMap
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
from PyQt5.QtCore import QTimer,QDateTime
from branca.element import Figure
from PyQt5.QtCore import QTimer
from folium.plugins import MarkerCluster
MarkerCluster()

READ_API_KEY='ZG0YZXYKP9LOMMB9'
CHANNEL_ID= '1370649'


while True:
        with urllib.request.urlopen("http://api.thingspeak.com/channels/1370649/feeds/last.json?api_key=ZG0YZXYKP9LOMMB9%22") as url:
            s=url.read()
            response = s
            data=json.loads(response)
            msg1 = data['field1']
            msg2 = data['field2']
            print (msg1 +" ," + msg2)
            time.sleep(10)
