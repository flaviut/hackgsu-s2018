import requests
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

print "Python script started"
while True:
    print ser.readline()
    #needs to be parsed into accel values and capacitance
    # if accelerometer in the z plane = around 1 g then record capacitance and send to server 

