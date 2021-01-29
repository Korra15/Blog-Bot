#include <Servo.h>
long duration;
int distance;
Servo servo;
void setup() {
  // put your setup code here, to run once:
   pinMode(2, OUTPUT); // Sets the trigPin as an OUTPUT
   pinMode(3, INPUT); // Sets the echoPin as an INPUT
   Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
   servo.write(0);  //close cap on power on
    delay(100);
    servo.detach();
   Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
   Serial.println("with Arduino UNO R3");
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(2, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(2, HIGH);
  delayMicroseconds(10);
  digitalWrite(2, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(3, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
if (distance < 5) {
Serial.println("the distance is less than 5");
servo.attach(9);
servo.attach(8);
servo.write(0);
servo.write(0);
delay(1000);
servo.write(180);
servo.write(180);
delay(1000);
servo.detach();
servo.detach();
}
delay(500);
}
