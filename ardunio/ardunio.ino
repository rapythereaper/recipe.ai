long microsecondsToInches(long microseconds) {
   return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}
const int pingPin = 7; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 6; // Echo Pin of Ultrasonic Sensor

long getDepth(){
   long duration, inches, cm;
   pinMode(pingPin, OUTPUT);
   digitalWrite(pingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   pinMode(echoPin, INPUT);
   duration = pulseIn(echoPin, HIGH);
   inches = microsecondsToInches(duration);
   cm = microsecondsToCentimeters(duration);
   //Serial.print(inches);
   //Serial.print("in, ");
   //Serial.print(cm);
   //Serial.print("cm");
   //Serial.println();
  return inches;
   
}

void setup() {
  Serial.begin(57600);
  Serial.println("Ardunio Ready");

}

void loop() {
  if(Serial.available()){
    String command= Serial.readString();
    Serial.print(command);
    if(command.equals("G-D*2\n")){
      long inch=getDepth();
      Serial.print(inch);
      Serial.print("\n");
    }  

  }
  delay(1000*2);

}
