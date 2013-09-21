#include <SerialStream.h>
#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

using namespace std;
using namespace LibSerial;

#define NONE (0)
#define FWD  (1)
#define REV  (2)
#define STOP (3)
#define HI (4)

#define SLEEP_TIME (1000*1000*1)
#define PORT "/dev/ttyUSB1"

SerialStream ardu;

struct Command{
  char cmd;
  char value;
};

void open(){
  /*The arduino must be setup to use the same baud rate*/ 
  ardu.Open(PORT);    
  ardu.SetBaudRate(SerialStreamBuf::BAUD_9600);  
}

void read(char *in, size_t numbytes){
  ardu.read(in,numbytes);
}

int read(char *in){
  ardu >> in;
  int res;
  sscanf(in,"%d",&res);
  return res;
}

void send(char *out, size_t numbytes){
  ardu.write(out,numbytes);
}

int sendCmd(char newCmd, char value){
  cout << "sending " << newCmd << "@" << value << endl;
  Command c;
  c.cmd = newCmd;
  c.value = value;
  send((char *)(void*)&c,sizeof(Command));
  char res[16];
  return read(res);
}

int main(int argc, char *argv[]){
  open();
  // wait for ardu to reset
  sleep(5);


  timespec sleeptime;
  sleeptime.tv_sec  = 0;
  sleeptime.tv_nsec = 100000000L;


    size_t cmd,value;  

    cout << "ramp up forwards" << endl;
    for(uint8_t i = 0; i < 256; i++){
      sendCmd(1,i);
      nanosleep(&sleeptime,NULL);
    }
    sleep(1);

    cout << "ramp down forwards" << endl;
    for(uint8_t i = 255; i >=0; i--){
      sendCmd(1,i);
      nanosleep(&sleeptime,NULL);
    }
    sleep(1);

    cout << "ramp up reverse" << endl;
    for(uint8_t i = 0; i < 256; i++){
      sendCmd(2,i);
      nanosleep(&sleeptime,NULL);
    }
    sleep(1);

    cout << "ramp down forwards" << endl;
    for(uint8_t i = 255; i >=0; i--){
      sendCmd(2,i);
      nanosleep(&sleeptime,NULL);
    }

    sendCmd(3,120);

  return 0;
}
