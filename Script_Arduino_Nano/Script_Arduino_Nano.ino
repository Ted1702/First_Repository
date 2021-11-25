#include <RF24.h>
#include<SPI.h>
#include<DigitalIO.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h> 
LiquidCrystal_I2C lcd(0x27,16,2);
RF24 radio(9,10);
const uint64_t add=0xF0F0F0F0E1LL;
const uint64_t add1=0xE7E7E7E7E7LL;
//ce = 9, csn = 10 pins
int16_t value_x=0,value_y=0,value_sw = 0, value_x1 = 0, value_y1 = 0, value_sw1 = 0;;
const int buttonPin = 4;
int buttonState ;
int buttonState_sw ;
void setup() {
Serial.begin(57600);
SPI.begin();
pinMode(A6, INPUT);
pinMode(A7, INPUT);
pinMode(A0, INPUT);
pinMode(A1, INPUT);
pinMode(2, INPUT_PULLUP);
pinMode(8, INPUT_PULLUP);
pinMode(buttonPin, INPUT_PULLUP);
digitalWrite(buttonState, HIGH);
radio.begin();
radio.setPALevel(RF24_PA_MIN);
radio.setChannel(0x76);
radio.setDataRate(RF24_1MBPS);
radio.setAutoAck(false);
//radio.printDetails();
radio.openWritingPipe(add) ;
radio.openReadingPipe(1,add1);
radio.enableDynamicPayloads();
radio.powerUp();
lcd.init();
lcd.backlight();
lcd.setCursor(0,0);
}

void loop() {
  radio.stopListening();
  float pos = 1000;
  delay(100);
  value_x = analogRead(A6); 
  value_y = analogRead(A7); 
  value_sw1 = digitalRead(2);
  value_x1 = analogRead(A0); 
  value_y1 = analogRead(A1); 
  String text,s1,s2,s3,s4,a1,a2,a3;
  buttonState = digitalRead(buttonPin);
  buttonState_sw = digitalRead(2);
  if(buttonState==HIGH){
    if(value_x>470 && value_x<550 && value_y>470 && value_y<550)
    {
      a1="x"+String(int(value_x1+pos))+",";
      a2="y"+String(int(value_y1+pos))+",";
      if(buttonState_sw==LOW)
  a3="b"+String(1750)+",";
  else
  a3="r"+String(1000)+",";
  text="arm,"+a1+a2+a3;
  char mesaj[32];
  text.toCharArray(mesaj,32);
  Serial.println(mesaj);
  radio.write(&mesaj, sizeof(mesaj));
  delay(500);
    }
    else
    {
  if(value_x<470){
    s3="c0";
    s4="d"+String(int(abs(value_x-470)/4.71));
  }else if(value_x>550) {
    s3="c"+String(int((value_x-550)/4.74));
    s4="d0";
  }else{
    s3="c0";
    s4="d0";
  }
  if(value_y<470){
    s1="a0";
    s2="b"+String(int(abs(value_y-470)/4.71));
  }else if(value_y>550){
    s1="a"+String(int((value_y-550)/4.74));
    s2="b0";
  }else{
    s1="a0";
    s2="b0";
  }
  text="car,"+s1+","+s2+","+s3+","+s4+",";
  char mesaj[32];
  text.toCharArray(mesaj,32);
  Serial.println(mesaj);
  radio.write(&mesaj, sizeof(mesaj));
  delay(500);
    }
  }else{
    char a[32]="stop";
    radio.write(&a, sizeof(a));
    delay(200);
    radio.startListening();
    delay(200);
    if(radio.available()){
      while(radio.available()){
      char text1[32]={0};
      radio.read(&text1, sizeof(text1));
      //String copie(text);
      Serial.println(text1);
      lcd.clear();
      lcd.print(text1);
      radio.stopListening();
      }
    }
    delay(500);
  
}
}
