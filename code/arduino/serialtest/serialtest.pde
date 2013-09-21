#include <NewSoftSerial.h>
#include <LiquidCrystal.h>
#include <LCDKeypad.h>

NewSoftSerial mySerial(0,1);

LCDKeypad lcd;
void setup()  
{
  mySerial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();
}

char buf[255];

void loop() // run over and over
{

  buf[0] = 'f';
  buf[1] = 'a';
  buf[2] = 'c';
  buf[3] = 'e';
  buf[4] = '\n';
  int i = 0;
  bool found = false;
  lcd.clear();
  lcd.setCursor(0,0);
  while(mySerial.available()){
    buf[i] = mySerial.read();
    found = true;
    lcd.print(buf[i]);
    i++;
  }
  if(found){
    mySerial.print(buf);
    mySerial.flush();
  } 
  /*else{  
    mySerial.print("nothing");
    mySerial.print("\n");
  }
  */
  delay(100);


}
