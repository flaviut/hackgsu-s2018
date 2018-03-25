import requests
import serial

previousWaterLevel = 0.0
waterLevel = 0.0
firstRun = True
ser = serial.Serial('/dev/ttyACM0', 9600)
def sendInfo(level):
        #send .33, .66, or 1.
        if(level < 1000):
            waterLevel = 0.00
        elif (level > 1000 and level <3000):
            waterLevel = 0.25
        elif (level > 3000 and level < 5000):
            waterLevel = 0.50
        elif (level > 5000 and level < 6800):
            waterLevel = 0.75
        else: 
            waterLevel = 1.00
        if(firstRun != True and previousWaterLevel != waterLevel):    
            r = requests.post('http://54.175.172.96/add', data= {"level": waterLevel})
        else:
            r = requests.post('http://54.175.172.96/add', data= {"level": waterLevel})
        print r
        print waterLevel
average_cap = 0
total_cap = 0
upright_samples = 0
bottle_is_upright = False
print "Python script started"
while True:
    data = ser.readline().split(",")
    capacitance = float(data[0].strip())
    accelX = float(data[1].strip())
    accelY = float(data[2].strip())
    accelZ = float(data[3].strip())

    print "Capacitance:\t%.2f\nAccel X:\t%.2f\nAccel Y:\t%.2f\nAccel Z:\t%.2f" % (capacitance, accelX, accelY, accelZ)

    if (accelX < -0.8 and accelX > -1.2):  #is -x because  we have our thing oriented weird
        upright_samples += 1
	total_cap += capacitance
    else:
        upright_samples = 0
	total_cap = 0

    if (upright_samples >= 3):
        bottle_is_upright = True
	average_cap = total_cap / 3
        sendInfo(average_cap)
	upright_samples = 0
	total_cap = 0
    else:
        bottle_is_upright = False

