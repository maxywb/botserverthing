// drive modes
#define FWD  (1)
#define REV  (2)
#define STOP (3)
// motor faults
#define NONE 0
#define SHORT 1
#define OVER_TEMP 2
#define UNDER_VOLT 3
#define UNKNOWN -2
// motor pins
#define DIR 8 
#define PWM 9
#define RESET 10
#define FF1 11
#define FF2 12

uint8_t readFault(){
  uint8_t ff1 = digitalRead(FF1);
  uint8_t ff2 = digitalRead(FF2);

  if(ff1+ff2 == 0){
    return NONE;
  }else if(ff1+ff2 == 1){
    if(ff1 == HIGH)
      return OVER_TEMP;
    else
      return SHORT;
  }else if(ff1+ff2 == 2){
    return UNDER_VOLT;
  }else{
    return -2;
  }
}

uint8_t resetMotor(){
  digitalWrite(RESET,LOW);
  delay(100);
  digitalWrite(RESET,HIGH);
  return readFault();
}

uint8_t motorSetup(){
  
  pinMode(DIR,OUTPUT);
  pinMode(PWM,OUTPUT);
  pinMode(RESET,OUTPUT);
  pinMode(FF1,INPUT);
  pinMode(FF2,INPUT);

  return resetMotor();
}

/*
 * drives the motor using locked-antiphase control
 */
uint8_t drive(uint8_t dir, uint16_t speed){
  if(speed > 128)
    return -1;
  
  switch(dir){
  case FWD:
    digitalWrite(PWM,HIGH);
    analogWrite(DIR,128+speed);
    break;
  case REV:
    digitalWrite(PWM,HIGH);
    analogWrite(DIR,128-speed);
    break;
  case STOP:
    digitalWrite(PWM,HIGH);
    analogWrite(DIR,128);
    break;
  default: // if i don't understand what's going on, why should i drive?
    digitalWrite(PWM,HIGH);
    analogWrite(DIR,128);
    break;
  }
  return readFault();
}

uint8_t curFault;
void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Motor test!");
  motorSetup();
}

void loop() {
  Serial.println("fwd");
  digitalWrite(RESET,LOW);
  digitalWrite(DIR,HIGH);
  analogWrite(PWM,128);
  digitalWrite(RESET,HIGH);
  curFault = readFault();
  Serial.print("fault: ");
  Serial.println(curFault,DEC);
  delay(1000);

  Serial.println("rev");
  digitalWrite(RESET,LOW);
  digitalWrite(DIR,LOW);
  analogWrite(PWM,128);
  digitalWrite(RESET,HIGH);
  curFault = readFault();
  Serial.print("fault: ");
  Serial.println(curFault,DEC);
  delay(1000);
}
