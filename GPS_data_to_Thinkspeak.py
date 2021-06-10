# bu kod python 3 ve üzeri sürüm gerektirir
# gerekli kütüphaneler kurulmalıdır.

import http.client, urllib.request, urllib.parse, urllib.error
import time
from GPS_API import *
import serial

ser = serial.Serial("/dev/serial0")  # Select Serial Port
ser.baudrate = 9600  # Baud rate
ser.timeout = 0.5
sleep = 10 # how many seconds to sleep between posts to the channel

key = "OM03HL3O0O4XOSNF"  # Thingspeak Write API Key
msgdata = Message() # Creates a Message Instance

def upload_cloud():
    temp = get_latitude(msgdata) # gps apı den gelen verileri tutuyoruz.
    temp1 = get_longitude(msgdata) # 
    params = urllib.parse.urlencode({'field1': temp,'field2': temp1, 'key':key }) # bu alınan verileri thingspeak channel ına bunları ekliyorum yani pars edioyprum
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept" : "text/plain"} # başlık tanımlıyorum
    conn = http.client.HTTPConnection("api.thingspeak.com:80") #  thing speak teki server a bağlantı sağlıyoruz.
    try: # post edebilmek için yani thing speak server ına connection isteği atıyorum. 25 te cevabı response ta tutuyorum.
        conn.request("POST", "/update", params, headers) 
        response = conn.getresponse()
        print(("Lat:",temp))
        print(("Long:",temp1))
        print((response.status, response.reason)) # statu ye bakıyoruz yüklenip yüklenemediğini kontrol ediyorum.
        conn.close() # connection ı kapatıyorum
    except KeyboardInterrupt:
         print("Connection Failed")  # hata mesajını print ediyorum           
             
if __name__ == "__main__": # gps reciever ı çalıştırıyor
    start_gps_receiver(ser, msgdata) # gps ı başlat serial port üzerinden oradaki verileri alıyoruz. gpS API  ztn tanımlamıştık oradan buraya geri gelicek.
    time.sleep(10) # delay 10 sn 
    ready_gps_receiver(msgdata) #  veriler alındımı diye kontrol etmiştik gps apı kodumuzda, veriler gelirse uploud cloud u çağırmama ve true döndürmeme vesile oluyor
    while True:  # delay süremize döngü başlatıyor.
        upload_cloud() #
        time.sleep(sleep) #


