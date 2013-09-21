

int pin = 7;
unsigned long duration;

void setup()
{
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  Serial.begin(9600);
  pinMode(6,OUTPUT);
  digitalWrite(6,HIGH);
}
unsigned long ctr = 0;
void loop()
{
  Serial.print(ctr++,DEC);  
  Serial.print(": ");
  Serial.println(pulseIn(8, HIGH));
  Serial.print(" ");
  Serial.println(pulseIn(9, HIGH));
}
