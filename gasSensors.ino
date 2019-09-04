#define MQ2pin (0)
#define MQ7pin (1)

float MQ2Value;
float MQ7Value;

void setup() {
  Serial.begin(9600);
  delay(20000); //20 seconds warm up period
}

void loop() {
  MQ2Value = analogRead(MQ2pin);
  Serial.write((byte)MQ2Value);
  delay(1000);
  MQ7Value = analogRead(MQ7pin);
  Serial.write((byte)MQ7Value);
  delay(1000); 
}
