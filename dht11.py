import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
DHT11_pin = 4

humidity, temperature = Adafruit_DHT.read_retry(11, DHT11_pin)
if humidity is not None and temperature is not None:
  print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
  print('Failed to get reading from the sensor. Try again!')

