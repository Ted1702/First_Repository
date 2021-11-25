import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import pigpio
import time
import spidev
pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)
'''
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
servo1 = GPIO.PWM(27,50) # pin 11 for servo1, pulse 50Hz
servo2 = GPIO.PWM(22,50)
servo3 = GPIO.PWM(5,50)
# Start PWM running, with value of 0 (pulse off)
servo1.start(0)
servo2.start(0)
servo3.start(0)
'''
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(False)
radio.enableDynamicPayloads()
radio.enableAckPayload()
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.startListening()
string1= list("raspuns")
while len(string1) < 32:
    string1.append(0)
while True:
    ackPL = [1]
    while not radio.available(0):
      time.sleep(0.01)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    string = ""
    for n in receivedMessage:
        if (n >= 32 and n <= 126) :
            string +=chr(n)
    print(string)
    x=string.split(",")
    a1=x[0]
    a2=x[1]
    a3=x[2]
    a1=a1[1:]
    a2=a2[1:]
    a3=a3[1:]
    pi.set_servo_pulsewidth(27,int(a1))
    pi.set_servo_pulsewidth(22,int(a2))
    pi.set_servo_pulsewidth(5,int(a3))
    pi.set_servo_pulsewidth(27,0)
    pi.set_servo_pulsewidth(22,0)
    pi.set_servo_pulsewidth(5,0)
    time.sleep(0.5)
    if(string=="stop"):
        radio.stopListening()
        time.sleep(0.2)
        radio.write(string1)
        print(string1)
        radio.startListening()
    
    

