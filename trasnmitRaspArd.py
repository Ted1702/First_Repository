import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
GPIO.setmode(GPIO.BCM)
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
    if(string=="stop"):
        radio.stopListening()
        time.sleep(0.2)
        radio.write(string1)
        print(string1)
    radio.startListening()
    