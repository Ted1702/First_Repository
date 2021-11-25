import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
in1 = 24
in2 = 23
enA = 25
in3 = 20
in4 = 16
enB = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
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
p=GPIO.PWM(enA,255)
q=GPIO.PWM(enB,255)
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
    if(string=="stop"):
        radio.stopListening()
        time.sleep(0.2)
        radio.write(string1)
        print(string1)
        radio.startListening()
    else:
        x = string.split(",")
        s1 = x[0]
        s2= x[1]
        s3 = x[2]
        s4 = x[3]
        s1 = s1[1:]
        s2 = s2[1:]
        s3 = s3[1:]
        s4 = s4[1:]
        grad1 = int(s1)
        grad2 = int(s2)
        grad3 = int(s3)
        grad4 = int(s4)
        if(grad1>0):
            if(grad3 == 0 and grad4 == 0):
                p.start(grad1)
                q.start(grad1)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
            elif(grad3 > 0):
                p.start(grad3)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
            elif(grad4>0):
                q.start(grad4)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
        
        elif(grad2>0):
            if(grad3 == 0 and grad4 == 0):
                p.start(grad2)
                q.start(grad2)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in4,GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
            elif(grad3>0):
                p.start(grad3)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
            elif(grad4>0):
                q.start(grad4)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
        else:
             GPIO.output(in1,GPIO.LOW)
             GPIO.output(in3,GPIO.LOW)
             GPIO.output(in2,GPIO.LOW)
             GPIO.output(in4,GPIO.LOW)
             p.stop()
             q.stop()
        radio.startListening()
