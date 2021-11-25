#include <Servo.h>
#define SERVO_PIN 6
int16_t value_x=0,value_y=0;
const int value_sw = 2;
int buttonState ;
Servo myservo1 ;
Servo myservo2 ;
void setup() {
Serial.begin(57600);
pinMode(A0, INPUT);
pinMode(A1, INPUT);
pinMode(value_sw, INPUT_PULLUP);
digitalWrite(value_sw, HIGH);
myservo1.attach(6);
myservo2.attach(5);
}

void loop() {
  value_x = analogRead(A0);
  //Serial.println(value_x);
  value_y = analogRead(A1);
  //Serial.println(value_y);
  float pos = 1024/180;
  buttonState = digitalRead(value_sw);
  if(buttonState==HIGH)
  {
  myservo1.write(int(value_x/pos));
  delay(50);
  myservo2.write(int(value_y/pos));
  delay(50);
  buttonState = digitalRead(value_sw);
  }
  else if(buttonState==LOW)
  {
   myservo1.write(0);
   delay(50);
   myservo2.write(0); 
   delay(2000);
  }
}
