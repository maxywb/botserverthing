#include <SerialStream.h>
#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
using namespace std;
using namespace LibSerial;

#define PING (255)
#define NONE (0)
#define FWD  (1)
#define REV  (2)
#define STOP (3)
#define STEER (4)
#define RESET (5)

#define SLEEP_TIME (1000*1000*1)
#define PORT "/dev/ttyUSB0"

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

void sendCmd(char newCmd, char value){
  cout << "sending " << newCmd << "@" << value << endl;
  Command c;
  c.cmd = newCmd;
  c.value = value;
  send((char *)(void*)&c,sizeof(Command));
}

int main(int argc, char *argv[]){
  open();
  // wait for ardu to reset
  sleep(5);
    char buf[256];
  while(true){
    memset(buf,0,256);
    buf[0] = 'a';
    buf[1] = 's';
    buf[2] = 'd';
    buf[3] = 'f';

    cout << "sending: " << buf << endl;
    ardu.write(buf,256);
    
    ardu.read(buf,256);
    cout << "got :" << buf << endl;

    usleep(1000*1000);
  }
  return 0;
}
