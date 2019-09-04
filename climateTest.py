# 3D PRINTER WIRELESS CLIMATE CONTROL SYSTEM PLUGGIN
# BY RYAN JAMES WALDEN & JUSTIN DANIEL HROMALIK

# Note: GPIOs are pins on the Raspberry Pi (RPi) that can be read or witten to.
# By wirring the pins to devices like switches or relays, you can control
# embedded systems like fans, motors, heaters, etc. Additionally you can
# read data being sent through a pin and use that to make inferences about
# the environment ie sensors.

#from __future__ import absolute_import
#import octoprint.plugin        # Integrates this program into OctoPrint as a plugin
import Adafruit_DHT             # Used for the DHT11 Sensors
import RPi.GPIO as GPIO         # RPi GPIO library
from serial import Serial       # Used to communicate with the Arduino UNO
from time import sleep          # Used to delay the program during runtime

# READABILITY ENHANCERS
# No need to change these values
HUMIDITY        = 0
TEMPERATURE     = 1
TOP             = 0             # denotes the top or 'second floor' of the enclosure
BOTTOM          = 1             # denotes the bottom or 'first floor' of the enclosure
OFF             = GPIO.LOW      # by setting a GPIO pin low you are turning it off
ON              = GPIO.HIGH     # by setting a GPIO pin high you are tuning it on

# TEMPERATURE & HUMIDITY
# To tune the system you will likely want to change the defaults, thresholds and delays
# GPIOs : 2,3,14,15
DHT_MODEL       = 11    # DHT11 temperature sensors will be used in this enclosure
BOT_DHT_GPIO    = 2     # GREEN controls bottom DHT11 sensor, no resitors required
TOP_DHT_GPIO    = 3     # PURPLE controls top DHT11 sensor, no resistors required
THRESHOLD       = 5     # the maximum deviation of the enclosure's climate temperature & humidity
TH_DELAY        = 5     # the length of the delay in testHeater and testDehumidifier
HEAT_GPIO       = 14    # WHITE controls the IoT Relay, which will turn the Lasko #100 heater on and off
DEFAULT_TEMP    = 30    # default target temperature of the enclosure
DEHUM_GPIO      = 15    # controls the dehumidifier, this will run off a simple relay for the MVP
DEFAULT_HUM     = 35    # default target humidity % of the enclosure

# GAS SENSORS
# All of these sensors have 4 pins but we will not be utilizing the digital out pin in any of them
# This will not be done on the RPi because the RPi can't read Analog outputs so I will need to wire these
# to an arduino then send the serial data over to the RPi via USB
USB_PORT = "/dev/ttyACM0"       # Top Left Port
BAUD_RATE = 9600        # Standard speed communication

# BYPASS VALVES
# No need to change these values
# GPIOs : 5,6
VALVE_DELAY     = 1     # the length of the delay in testValves
CLICKS          = 3     # the number of clicks the bypass valve(s) will make in testValves
BOT_VALVE_GPIO  = 5     # controls the bottom bypass valve relay
TOP_VALVE_GPIO  = 6     # controls the top bypass valve relay

# SETUP GPIO SYSTEM
# DHT_GPIOs do not need to be setup, because setup is handled in the Adafruit_DHT module
GPIO.setwarnings(False) # Ignore warnings for now
GPIO.setmode(GPIO.BCM)  # Use GPIO Port numbering system
GPIO.setup(HEAT_GPIO, GPIO.OUT)         # Set HEAT_GPIO to be an output pin and set initial value to low (off)
# The following systems run off the 8 channel relay which is active low, therefore we must set these pins HIGH
GPIO.setup(DEHUM_GPIO, GPIO.OUT)        #Set DEHUM_GPIO to be an output pin and set initial value to high (on)
GPIO.output(DEHUM_GPIO, ON)
GPIO.setup(BOT_VALVE_GPIO, GPIO.OUT)    # Set BOT_VALVE_GPIO to be an output pin and set initial value to high (on)
GPIO.output(BOT_VALVE_GPIO, ON)
GPIO.setup(TOP_VALVE_GPIO, GPIO.OUT)    # Set TOP_VALVE_GPIO to be an output pin and set initial value to high (on)
GPIO.output(TOP_VALVE_GPIO, ON)

# Obtain current Temperature or Humidity
def getDHT(topOrBottom, humOrTemp):
        if(topOrBottom == TOP):
                DHT_GPIO = TOP_DHT_GPIO
        elif(topOrBottom == BOTTOM):
                DHT_GPIO = BOT_DHT_GPIO
        else:
                return "Error: Invalid parameter for topOrBottom."

        humidity, temperature = Adafruit_DHT.read_retry(DHT_MODEL, DHT_GPIO)

        if(humOrTemp == HUMIDITY):
                return humidity
        elif(humOrTemp == TEMPERATURE):
                return temperature
        else:
                return "Error: Invalid parameter for humOrTemp."

# Test the bypass valve(s)
def testValves(topOrBottom):
        if(topOrBottom == TOP):
                VALVE_GPIO = TOP_VALVE_GPIO
        elif(topOrBottom == BOTTOM):
                VALVE_GPIO = BOT_VALVE_GPIO
        else:
                return "Error: Invalid parameter for topOrBottom."

        for i in range(CLICKS):
                GPIO.output(VALVE_GPIO, OFF)
                sleep(VALVE_DELAY)
                GPIO.output(VALVE_GPIO, ON)
                sleep(VALVE_DELAY)

# Heat the enclosure if it not within the target threshold
def setTemp(target):
        current = getDHT(BOTTOM, TEMPERATURE)
        if(current > target + THRESHOLD):
                GPIO.output(HEAT_GPIO, OFF)
                return True
        else:
                return False

# Heat the enclosure until it is within the target threshold
def testHeater(targetTemperature):
        GPIO.output(HEAT_GPIO, ON)
        while(not setTemp(targetTemperature)):
                sleep(TH_DELAY)
        GPIO.output(HEAT_GPIO, OFF)
        return getDHT(BOTTOM, TEMPERATURE)

# Dehumidify the enclosure if humidity is not within the target threshold
def setHum(target):
        current = getDHT(BOTTOM, HUMIDITY)
        while(current > target - THRESHOLD):
                sleep(TH_DELAY)
                current = getDHT(BOTTOM, HUMIDITY)
        return True

# Dehumidify the enclosure until it is within the target threshold
def testDehumidifier(targetHumidity):
        GPIO.output(DEHUM_GPIO, OFF)
        setHum(targetHumidity)
        GPIO.output(DEHUM_GPIO, ON)
        return getDHT(BOTTOM, HUMIDITY)

# Detect the current enclosure air contents
def testAirContent():
        print("Gas sensors warming up for 20 seconds...")
        arduinoSerial = Serial(USB_PORT, BAUD_RATE)
        arduinoSerial.flushInput()
        serialSent = False

        i = 0
        while not serialSent:
                if arduinoSerial.inWaiting()>0:
                        output = arduinoSerial.read(1)
                        print(ord(output))
                        i = i + 1
                        if (i == 2):
                                serialSent = True
                                return "Success"

print("Current Printer Enclosure Temperature (Celcius): " + str(getDHT(BOTTOM,TEMPERATURE)))
print("Current Printer Enclosure Humidity: " + str(getDHT(BOTTOM, HUMIDITY)))
#print("Current Spool Enclosure Temperature (Celcius): " + str(getDHT(TOP,TEMPERATURE)))
#print("Current Spool Enclosure Humidity: " + str(getDHT(TOP, HUMIDITY)))
print("Testing Enclosure Air Content: ")
testAirContent()
print("Testing Dehumidifier Bypass Valve (listen for 3 clicks from the bottom of the enclosure): ")
testValves(BOTTOM)
print("Testing Dehumidifier Bypass Valve (listen for 3 clicks from the top of the enclosure): ")
testValves(TOP)
print("Testing Heater (Heating Enclosure...): " + str(testHeater(int(getDHT(BOTTOM,TEMPERATURE)))))
print("Testing Dehumidifier (Dehumidifying Enclosure...): " + str(testDehumidifier(int(getDHT(BOTTOM,HUMIDITY)))))
print("Initiating Climate Control...")

