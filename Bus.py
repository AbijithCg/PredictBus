import RPi.GPIO as GPIO
import time
import thread
import telegram
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pynmea import nmea
from geopy.geocoders import GoogleV3
import serial

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,0)   #LED
GPIO.output(40,0)

address='Checking Location...'
lat='0'
lon='0'

ser = serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=1)

geocoder = GoogleV3()
def gps(threadName, delay):
    global address,lat,lon
    while(1):
        gps_data=ser.read(350)
    
        try:
                if 'GPRMC' in gps_data:
                    z=gps_data.index('GPRMC')
                    lats=gps_data[z+19:z+28]
                    longs=gps_data[z+31:z+41]
                    lat1=(float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
                    lat=(float(lats[0]+lats[1])+lat1)
                    long1=(float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
                    lon=(float(longs[0]+longs[1]+longs[2])+long1)
                    
                    print 'latitude=',lat
                    print 'longitude=',lon
                    
                    location_list = geocoder.reverse(str(lat)+','+str(lon))
                    location = location_list[0]
                    address = location.address
                    print address
                    print '***************************************************************'
                    GPIO.output(40,1)
        except:
            print 'No GPS Data'
            GPIO.output(40,0)
        


def position(bot, update):
    l='!!!Bus Position!!!\n'+address+'\nLatitude='+lat+'\nLongitude='+lon
    update.message.reply_text(l)

bot = telegram.Bot(token='321526530:AAFt5njA-tb3r1l78kwxsxo6E7YHt0CI_wE')
updater = Updater('321526530:AAFt5njA-tb3r1l78kwxsxo6E7YHt0CI_wE')


updater.dispatcher.add_handler(CommandHandler('position', position))  


try:    
   thread.start_new_thread(gps, ("Thread-1", 1, ) )
   updater.start_polling()
   updater.idle()
  
except:
   print "Error: unable to start thread"

while 1:
   pass
