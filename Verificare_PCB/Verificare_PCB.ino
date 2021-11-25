#include <RF24.h>
#include<SPI.h>
#include<DigitalIO.h>
#include<AESLib.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h> 
RF24 radio(9,10);
LiquidCrystal_I2C lcd(0x27,16,2);
const uint64_t add=0xF0F0F0F0E1LL;
const uint64_t add1=0xE8E8F0F0E1LL;
//ce = 9, csn = 10 pins
int16_t value_x = 0, value_y = 0, value_sw = 0, value_x1 = 0, value_y1 = 0, value_sw1 = 0;
const int buttonPin = 6;
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
digitalWrite(buttonPin, HIGH);
radio.begin();
radio.setPALevel(RF24_PA_MAX);
radio.setChannel(0x76);
radio.setDataRate(RF24_1MBPS);
radio.setAutoAck(false);
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
  value_sw = digitalRead(2);
  value_x1 = analogRead(A0); 
  value_y1 = analogRead(A1); 
  value_sw1 = digitalRead(8);
  String text,a1,a2,a3;
  buttonState = digitalRead(buttonPin);
  buttonState_sw = digitalRead(2);
  if(buttonState==HIGH){
  //if(value_x<490 ||  value_x>525)
    a1="x"+String(int(value_x+pos))+",";
  //else if(value_y<490 || value_y>525)
   a2="y"+String(int(value_y+pos))+",";
  if(buttonState_sw==LOW)
  a3="b"+String(1500)+",";
  else
  a3="r"+String(1000)+",";
  text=a1+a2+a3;
  char mesaj[32];
  text.toCharArray(mesaj,32);
  Serial.println(mesaj);
  radio.write(&mesaj, sizeof(mesaj));
  delay(500);
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
      Serial.println(text1);
      lcd.clear();
      lcd.print(text1);
      radio.stopListening();
      }
    }
    delay(500);
  
}
}
