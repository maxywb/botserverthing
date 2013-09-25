#include <SerialStream.h>
#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

using namespace std;
using namespace LibSerial;

#define PING (6)
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
  cout << "reading" << endl;
  ardu >> in;
  int res;
  sscanf(in,"%d",&res);
  return res;
}

void send(char *out, size_t numbytes){
  ardu.write(out,numbytes);
}

void sendCmd(char newCmd, char value){

  Command c;
  c.cmd = newCmd;
  c.value = value;
  printf("sending %x-%x(%ld)",c.cmd,c.value,sizeof(c));
  send((char *)(void*)&c,sizeof(Command));
  printf("   sent\n");
}

int main(int argc, char *argv[]){
  open();
  // wait for ardu to reset
  sleep(5);

  while(true){
    size_t cmd,value;  
    cout << "enter cmd: ";
    cin >> cmd;
    cout << endl << "enter value: ";
    cin >> value;
    cout << endl;

    switch(cmd){
    case FWD:
    case REV:
      if(value > 128){
	cout << "value too big" << endl;
	continue;
      }    
      break;
    case STEER:
      if(value > 180){
	cout << "value too big" << endl;
	continue;
      }    
      break;
    case STOP:
    case PING:
    case NONE:
    default:
      break;
    }

    sendCmd(cmd&0xff,value&0xff);

    char back[255];
    printf("got back: ");
    read(back);
    //    cout << back << endl;
    
    for(int i = 0; i < 255; i++){
      printf("%c-",back[i]);
    }
    printf("\n");
    
  }
  return 0;
}
