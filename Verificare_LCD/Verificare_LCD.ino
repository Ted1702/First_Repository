LiquidCrystal_I2C lcd(0x27,16,2);
void setup() {
  // put your setup code here, to run once:
lcd.init();
lcd.backlight();
lcd.setCursor(0,0);
}
String text = "Hello World";
void loop() {
  // put your main code here, to run repeatedly:
lcd.clear();
delay(500);
lcd.print(text);
}
