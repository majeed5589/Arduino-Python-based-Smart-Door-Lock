#include <Servo.h>

Servo myservo;       // Create a servo object
char d;              // Variable to store incoming serial data
int pos;             // Variable to store servo position

void setup() {
  Serial.begin(9600);      // Initialize serial communication at 9600 bits per second
  myservo.attach(9);       // Attach the servo on pin 9 to the servo object
  myservo.write(0);        // Set servo to initial position
  pinMode(13, OUTPUT);     // Set pin 13 (built-in LED) as an output
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available()) {
    d = Serial.read();     // Read the incoming character
  }

  // If the character 'a' is received
  if (d == 'a') {
    Serial.print(d);       // Echo the received character back (optional)

    // Blink the built-in LED for 1 second ON and 1 second OFF
    digitalWrite(13, HIGH);  // Turn the LED on
    delay(1000);             // Wait for 1 second
    digitalWrite(13, LOW);   // Turn the LED off
    delay(1000);             // Wait for 1 second
     digitalWrite(13, HIGH);  // Turn the LED on
    delay(1000);             // Wait for 1 second
    digitalWrite(13, LOW);   // Turn the LED off
    delay(1000);             // Wait for 1 second
     digitalWrite(13, HIGH);  // Turn the LED on
    delay(1000);             // Wait for 1 second
    digitalWrite(13, LOW);   // Turn the LED off
    delay(1000);             // Wait for 1 second

    // Move the servo to open the door
    for (pos = 0; pos <= 90; pos += 5) {
      myservo.write(pos);    // Move the servo to the current position
      delay(20);             // Wait for 20 milliseconds
    }

    delay(5000);             // Keep the door open for 5 seconds

    // Move the servo back to close the door
    for (pos = 90; pos >= 0; pos -= 5) {
      myservo.write(pos);    // Move the servo to the current position
      delay(20);             // Wait for 20 milliseconds
    }

    d = 0;                   // Reset the character variable
  }
}
