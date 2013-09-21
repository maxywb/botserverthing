// drive modes
#define FWD  (1)
#define REV  (2)
#define STOP (3)
// motor pins
#define MOTOR (10)

void motorSetup(){
  pinMode(MOTOR,OUTPUT);
}

/*
 * drives the motor in locked antiphase mode
 * jumper 8 on mds40 controlls mode(sign magnitude vs locked antiphase)
 * and needs to be set to 0 for this function to work
 */
void drive(uint8_t dir, uint16_t speed){
  if(speed > 128)
    return;
  
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
}

void setup() {

  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  
  analogWrite(9,129);
  digitalWrite(8,HIGH);
}

void loop() {
  /*  Serial.println("fwd@128");
  drive(FWD,128);
  delay(1000);

  Serial.println("rev@128");
  drive(REV,128);
  delay(1000);

  Serial.println("stop");
  drive(STOP,0);
  delay(1000);
  */
}
