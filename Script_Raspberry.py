import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import pigpio
import time
import spidev
import Adafruit_DHT
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
PAGE="""\
<html>
<head>
<title>Pi Camera Streaming</title>
<style>
body {
  background-image: url(https://lh3.googleusercontent.com/proxy/p0rdn1qcalA3TIi9QkxOx-CgL_3bsjvRByOqI7Ynn6tYa7DCsIxex0uzd5smXW4p-ZASQ-xjiSUtp-tKVCuKe0epo5sPCJmWOOFRlRPyjzp_HMIhnfwzix6fouLpWQ995ixPiQxBjQ);
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
}
</style>
</head>
<body>
<center><h1>Pi Camera Streaming</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""


class StreamingOutput(object):
	def __init__(self):
		self.frame = None
		self.buffer = io.BytesIO()
		self.condition = Condition() 
	def write(self,buf):
		if buf.startswith(b'\xff\xd8'):
			self.buffer.truncate()
			with self.condition:
				self.frame = self.buffer.getvalue()
				self.condition.notify_all()
			self.buffer.seek(0)
		return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
			self.send_response(301)
			self.send_header('Location','/index.html')
			self.end_headers()
		elif self.path == '/index.html':
			content = PAGE.encode('utf-8')
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.send_header('Content-Length', len(content))
			self.end_headers()
			self.wfile.write(content)
		elif self.path == '/stream.mjpg':
			self.send_response(200)
			self.send_header('Age',0)
			self.send_header('Cache-Control', 'no-cache, private')
			self.send_header('Pragma', 'no-cache')
			self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
			self.end_headers()
			try:
				while True:
					with  output.condition:
						output.condition.wait()
						frame = output.frame
					self.wfile.write(b'--FRAME\r\n')
					self.send_header('Content-Type', 'image/jpeg')
					self.send_header('Content-Length', len(frame))
					self.end_headers()
					self.wfile.write(frame)
					self.wfile.write(b'\r\n')
			except Exception as e:
				logging.warning(
					'Removed streaming client %s: %s', selfclient_address, str(e))
		else:
			self.send_error(404)
			self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
	allow_reuse_address = True
	daemon_threads = True
with picamera.PiCamera(resolution = '640x480', framerate=24) as camera:
	output = StreamingOutput()
	#camera.rotation = 90
	camera.start_recording(output, format='mjpeg')
	try:
		address = ('192.168.1.114',8000)
		server = StreamingServer(address, StreamingHandler)
		server.serve_forever()
	finally:
		camera.stop_recording()
sensor = Adafruit_DHT.DHT11
DHT11_pin = 4
pi = pigpio.pi()
in1 = 24
in2 = 23
enA = 25
in3 = 20
in4 = 16
enB = 21
GPIO.setwarnings(False)
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
p=GPIO.PWM(enA,255)
q=GPIO.PWM(enB,255)
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
        humidity, temperature = Adafruit_DHT.read_retry(11, DHT11_pin)
        string1="T:"+str(temperature)+"C H:"+str(humidity)+"%"
        #while len(string1) < 32:
            #string1=string1+"0"
        radio.write(string1[0:15])
        print(string1)
        radio.startListening()
    else:
        x = string.split(",")
        if(x[0]=="car"):
            pi.set_servo_pulsewidth(27,1500)
            pi.set_servo_pulsewidth(22,1500)
            pi.set_servo_pulsewidth(5,1000)
            s1 = x[1]
            s2= x[2]
            s3 = x[3]
            s4 = x[4]
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
        if(x[0]=="arm"):
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            a1=x[1]
            a2=x[2]
            a3=x[3]
            a1=a1[1:]
            a2=a2[1:]
            a3=a3[1:]
            print(a3)
            pi.set_servo_pulsewidth(27,int(a1))
            pi.set_servo_pulsewidth(22,int(a2))
            pi.set_servo_pulsewidth(5,int(a3))
            #pi.set_servo_pulsewidth(27,0)
            #pi.set_servo_pulsewidth(22,0)
            #pi.set_servo_pulsewidth(5,0)
            time.sleep(0.2)
            radio.startListening()