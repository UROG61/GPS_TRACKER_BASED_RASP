# -*- coding: utf-8 -*-
"""
Created on Sat May 15 23:07:21 2021

@author: Selim Altıntaş
"""

import time
import json
import csv
import urllib.request
import os
import sys
import io
import folium # pip install folium
from folium.plugins import MiniMap
from folium import plugins
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from branca.element import Figure
from PyQt5.QtCore import QTimer
from folium.plugins import MarkerCluster
MarkerCluster()


#sleep = 2 # how many seconds to sleep between posts to the channel

  
# while True:
#     m1,m2 = read_cloud()
#     time.sleep(sleep)
    
class MyApp(QWidget): # qwidget pencerenin template ini hazırlıyor. MYapp in içinde Qwidget ı düzenliyorum.
    def __init__(self):
        super().__init__()
        global map_obj,url
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600,800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout() # widget ın içinde boxlayout oluşturuyorum ve aşağıda editliyorum
        self.setLayout(layout)
        df = pd.read_csv("https://data.ibb.gov.tr/en/dataset/7456b10e-1128-48f7-82f5-5503d98bfb1b/resource/f4f56e58-5210-4f17-b852-effe356a890c/download/ispark_parking.csv")
        locations = df[['LATITUDE', 'LONGITUDE']]
        locationlist = locations.values.tolist() # pandas a list olarak okuyabilmek için list olarak gelen veriyi çeviriyorum.
        len(locationlist)
        
        coordinate = (41.03659674666299, 28.83363416347736)
        map_obj = folium.Map(
        	tiles='cartodbpositron',
        	zoom_start=13,
        	location=coordinate
            )
        
        marker_cluster = MarkerCluster().add_to(map_obj) 
        for point in range(0, len(locationlist)): # location list in uzunluğu kadar folium da gösterilcek marker ın yerini  ve marker tipleri ve harita temaları ayarlıyorum
            folium.Marker(locationlist[point], popup=df['COUNTY_NAME'][point],icon=folium.Icon(color='green')).add_to(marker_cluster)
        folium.Marker(coordinate, popup='Baslama',width=400,height=400,icon=folium.Icon(color='red',prefix='glyphicon',icon='none')).add_to(map_obj)
        folium.TileLayer('cartodbpositron').add_to(map_obj) 
        folium.TileLayer('Stamen Toner').add_to(map_obj)
        folium.TileLayer('Stamen Water Color').add_to(map_obj)
        folium.TileLayer('Stamen Terrain').add_to(map_obj)
        folium.TileLayer('cartodbdark_matter').add_to(map_obj)
        folium.LayerControl().add_to(map_obj)
        
        mini_map = plugins.MiniMap(toggle_display=True)
        mini_map = MiniMap(tile_layer="cartodbpositron")
        map_obj.add_child(mini_map)
        map_obj
        
        # save map data to data object
        self.data = io.BytesIO() # bytes şeklinde veriyi oluşturuyorum sonra harita objesine bu sekilde kaydediyorum.
        map_obj.save(self.data, close_file=False) # save ledikten sonra açık kalmaya devam etmesi için

        
        self.webView = QWebEngineView()
        self.webView.setHtml(self.data.getvalue().decode())
        layout.addWidget(self.webView)
        
        
        
        urllib.timeout = 0.5
        
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.updateLocation)
        self.timer1.start(120000)

        
        
    def updateLocation(self):
        global url,map_obj # global her fonksiyonda kullanabilmemiz için
        m1,m2 = self.read_cloud()
        map_obj.location=[m1,m2]
        folium.Marker([m1,m2], popup='Selim',icon=folium.Icon(icon="car", prefix="fa"),zoom_start=15).add_to(map_obj)
        self.data.seek(0) 
        map_obj.save(self.data,close_file=False)
        self.webView.setHtml(self.data.getvalue().decode())
        print("OK")
        
    def read_cloud(self):
        global url
        url=urllib.request.urlopen("http://api.thingspeak.com/channels/1370649/feeds/last.json?api_key=ZG0YZXYKP9LOMMB9%22")
        data = json.loads(url.read())
        msg1 = data['field1']
        msg2 = data['field2']

        print(msg1,msg2)
        return msg1,msg2 # aldığım ve boylamı döndürüyor. bu olmasa fonksiyondan bilgilerin çıktısını başka fonksiyona alamayız.
        
        



if __name__ == '__main__':
    app = QApplication(sys.argv) # application tanımlıyorum
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp() # myapp i apllication ın içinde olusturuyorum
    myApp.show() # application ın içinde gösteriyorum

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')  
