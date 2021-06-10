#raspberry pi içindir gerekli ayarlar yapılmalı
import threading
import pynmea2
import sys

class Message:
    def __init__(self):
        self.msg ='' 

# Gps Receiver thread funcion, check gps value for infinite times
def get_gps_data(serial, dmesg): # porttan gelen veriyi mesaj olarak tanımlıyoruz
    print("Initializing GPS\n") #
    while True: #
        strRead = serial.readline() #
        if sys.version_info[0] == 3: # python varsayılan olarak 3 sürümü olduğuna bakıyoruz.
            strRead = strRead.decode("utf-8","ignore") # veriyi decode ediyoruz ve okunabilir bir hale getiriyoruz
            if strRead[0:6] == '$GPGGA':   #
                dmesg.msg = pynmea2.parse(strRead) #  okunan  str ın gpgga değeriyse bunu mesaj olarak bastrıyoruz
        else:   #
            if strRead.find('GGA') > 0: # 0 dan büyükse mesajı bastırıyoruz
                dmesg.msg = pynmea2.parse(strRead) # 

# API to call start the GPS Receiver
def start_gps_receiver(serial, dmesg):    # Gps in alıcısının başlayıp başlamadıgını kontrol ediyor ve başlıyor
    t2 = threading.Thread(target=get_gps_data, args=(serial, dmesg))  #
    t2.start()    #
    print("GPS Receiver started")   # 

# API to fix the GPS Revceiver
def ready_gps_receiver(msg):  # buraya gelen parametre "msg" olarak tanımlandı
    print("Please wait fixing GPS .....")  #
    dmesg = msg.msg #
    while(dmesg.gps_qual != 1): #  gps den gelen veriyi bakarak eğer bir hata yoksa gps fix available diye  mesajı yazıyor.
        pass
    print("GPS Fix available") #

# API to get latitude from the GPS Receiver
def get_latitude(msg): # 
    dmesg = msg.msg # 
    return dmesg.latitude #

# API to get longitude from the GPS Receiver
def get_longitude(msg):   #
    dmesg = msg.msg  #
    return dmesg.longitude  #
