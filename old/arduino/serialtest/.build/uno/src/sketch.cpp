#include <Arduino.h>
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
void setup();
void loop();
#line 1 "src/sketch.ino"
//#include <SoftwareSerial.h>
//#include <LiquidCrystal.h>

SoftwareSerial usb(0,1);

void setup()  
{
  usb.begin(9600);
  delay(1000);
}

typedef union{
  char raw[4];
  float   as_float;
  long as_int;
} cmd_contents;
typedef struct{
  char      cmd;
  cmd_contents data;
  char padding[3];
} packet;
typedef union{
  packet  nice;
  char raw[8];
}raw_packet;

void loop() // run over and over
{
  int i = 0;
  bool found = false;

  raw_packet com;

  while(usb.available()){
    found = true;
    if(i < 8){
      com.raw[i] = usb.read();
    } else{
      break;
    }
    i++;
  }

  if(!found){
    return;
  }

  packet curpacket = com.nice;

  if(curpacket.cmd = 1){
    usb.print("hi");
    usb.print("\n");
  }

}
