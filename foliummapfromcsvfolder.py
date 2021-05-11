
import time
import csv
import urllib.request
import os
import sys
import io
import folium # pip install folium
from folium import plugins
from folium.plugins import search
from folium.plugins import MiniMap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from branca.element import Figure
from PyQt5.QtCore import QTimer

#sleep = 2 # how many seconds to sleep between posts to the channel

  
# while True:
#     m1,m2 = read_cloud()
#     time.sleep(sleep)
    
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        global map_obj,url
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        

        coordinate = (41.03659674666299, 28.83363416347736)
        map_obj = folium.Map(
        	tiles='Stamen Terrain',
        	zoom_start=13,
        	location=coordinate
            )
      
      
        folium.Marker(coordinate, popup='Seattle',icon=folium.Icon(color='red',prefix='glyphicon',icon='none')).add_to(map_obj)
        folium.TileLayer('Stamen Terrain').add_to(map_obj)
        folium.TileLayer('Stamen Toner').add_to(map_obj)
        folium.TileLayer('Stamen Water Color').add_to(map_obj)
        folium.TileLayer('cartodbpositron').add_to(map_obj)
        folium.TileLayer('cartodbdark_matter').add_to(map_obj)
        folium.LayerControl().add_to(map_obj)
        
        # save map data to data object
        data = io.BytesIO()
        map_obj.save(data, close_file=False)

        
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)
        
        
        url = r'https://thingspeak.com/channels/1370649/feed.csv'
        urllib.timeout = 0.5
        print(url)
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.updateLocation)
        self.timer1.start(3000)

        
        
    def updateLocation(self):
        global url,map_obj
        m1,m2 = self.read_cloud()
        map_obj.location=[m1,m2]
        folium.Marker([m1,m2], popup='Seattle',icon=folium.Icon(color='red',prefix='glyphicon',icon='none')).add_to(map_obj)
        print("OK")
        
    def read_cloud(self):
        global url
        urllib.request.urlretrieve(url, '/Users/Selim Altıntaş/Desktop/Bitirme/Gps_tracker_grad/GPS_Data/1.csv')
        with open('/Users/Selim Altıntaş/Desktop/Bitirme/Gps_tracker_grad/GPS_Data/1.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                msg1=row[2]
                msg2=row[3]
        os.remove('/Users/Selim Altıntaş/Desktop/Bitirme/Gps_tracker_grad/GPS_Data/1.csv')
        print(msg1,msg2)
        return msg1,msg2
        
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')  
