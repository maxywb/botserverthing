#include <NewSoftSerial.h>
#include <LiquidCrystal.h>
#include <Servo.h>

struct Command{
  uint8_t cmd;
  uint8_t value;
};


#define NONE (0)
#define FWD  (1)
#define REV  (2)
#define STOP (3)
#define STEER (4)
#define RESET (5)
#define PING (6)

// motor pins
#define MOTOR (9)

// motor faults
#define NONE 0
#define SHORT 1
#define OVER_TEMP 2
#define UNDER_VOLT 3
#define UNKNOWN -2

// servo stuff
#define WHEEL_PIN (7)

#ifdef DEBUG
LCDKeypad lcd;
#endif

NewSoftSerial mySerial(0,1);
Command curCmd;
uint8_t curSpeed = 0;
Servo wheel;



/*
 * drives the motor using locked-antiphase control
 */
uint8_t drive(uint8_t dir, uint8_t speed){
  if(speed > 128)
    return -1;
  
  switch(dir){
  case FWD:
    analogWrite(MOTOR,128+speed);
    break;
  case REV:
    analogWrite(MOTOR,128-speed);
    break;
  case STOP:
    analogWrite(MOTOR,128);
    break;
  default: // if i don't understand what's going on, why should i drive?
    analogWrite(MOTOR,128);
    break;
  }
  return 0;
}

void steer(uint8_t direction){
  wheel.write(direction);
}

void replyCmd(){
  uint32_t response = 0xface0000;
  response = response | (curCmd.cmd << 16);
  response = response | (curCmd.value << 8);
  mySerial.println(response);
}

void setup()  
{
  // motor setup
  pinMode(MOTOR,OUTPUT);

  // steering setup
  wheel.attach(WHEEL_PIN);

  // communication setup
  mySerial.begin(9600);
}

void loop() // run over and over
{
  if (mySerial.available() >= sizeof(Command)){
    curCmd.cmd = mySerial.read();
    curCmd.value = mySerial.read();
    mySerial.flush();

  } else {
    curCmd.cmd = NONE;
    curCmd.value = -1;

  }

  switch(curCmd.cmd){
  case FWD:
    mySerial.print("drive_fwd\n");
    drive(FWD,curCmd.value);
    break;
  case REV:    
    mySerial.print("drive_rev\n");
    drive(REV,curCmd.value);
    break;
  case STOP:
    drive(STOP,0);    
    mySerial.print("stop\n");
    break;
  case STEER:
    steer(curCmd.value);
    mySerial.print("steer\n");
  case NONE:
    break;
  case PING:
    mySerial.println("hello_world");
    break;
  default:
    mySerial.println("default");
    break;
  }

  delay(1000);
}
