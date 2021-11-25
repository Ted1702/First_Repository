#include <RF24.h>
#include<SPI.h>
#include<DigitalIO.h>
#include<AESLib.h>
//#include "SdFat.h"
//#include <LiquidCrystal_I2C.h>
RF24 radio(9,10);
const uint64_t add=0xF0F0F0F0E1LL;
const uint64_t add1=0xE8E8F0F0E1LL;
//ce = 9, csn = 10 pins
int16_t value_x=0,value_y=0,value_sw = 0;
const int buttonPin = 4;
int buttonState ;
void setup() {
Serial.begin(57600);
SPI.begin();
pinMode(A6, INPUT);
pinMode(A7, INPUT);
pinMode(2, INPUT_PULLUP);
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
}

void loop() {
  radio.stopListening();
  delay(100);
  value_x = analogRead(A6); 
  value_y = analogRead(A7); 
  value_sw = digitalRead(2);
  String text,s1,s2,s3,s4;
  buttonState = digitalRead(buttonPin);
  if(buttonState==HIGH){
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
  text=s1+","+s2+","+s3+","+s4+",";
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
      //String copie(text);
      Serial.println(text1);
      radio.stopListening();
     /* sd.begin(8);
      myFile = sd.open("senzor.txt", FILE_WRITE);
      if (myFile) {
        myFile.println(copie); 
        myFile.close();
      } else {
        Serial.println("error opening senzor.txt");
      }
      lcd.clear();
      lcd.print(copie);*/
      }
    }
    delay(500);
  
}
}
