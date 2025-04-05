/*
  Button

  Turns on and off a light emitting diode(LED) connected to digital pin 13,
  when pressing a pushbutton attached to pin 2.

  The circuit:
  - LED attached from pin 13 to ground through 220 ohm resistor
  - pushbutton attached to pin 2 from +5V
  - 10K resistor attached to pin 2 from ground

  - Note: on most Arduinos there is already an LED on the board
    attached to pin 13.

  created 2005
  by DojoDave <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Button
*/

// constants won't change. They're used here to set pin numbers:
const int buttonPinP1 = 3;     // the number of the pushbutton pin for player 1
const int ledPinGreenP1 =  5;  // the number of the green LED pin for player 1
const int ledPinRedP1 = 2;     // the number of the red LED pin for player 1
const int buzzPinP1 =  4;      // the number of the buzzer pin for player 1
const int buttonPinP2 = 11;      // the number of the pushbutton pin for player 2
const int ledPinGreenP2=  10;    // the number of the green LED pin for player 2
const int ledPinRedP2 = 13;      // the number of the red LED pin for player 2
const int buzzPinP2 =  12;       // the number of the buzzer pin for player 2
int player = 0;

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

void setup() {
  // initialize the green LED player 1 pin as an output:
  pinMode(ledPinGreenP1, OUTPUT);
  // initialize the red LED player 1 pin as an output:
  pinMode(ledPinRedP1, OUTPUT);
  // initialize the pushbutton player 1 pin as an input:
  pinMode(buttonPinP1, INPUT);
  // initialize the buzzer player 1 pin as an output:
  pinMode(buzzPinP1, OUTPUT);
  // initialize the greenLED player 2 pin as an output:
  pinMode(ledPinGreenP2, OUTPUT);
  // initialize the red LED player 2 pin as an output:
  pinMode(ledPinRedP2, OUTPUT);
  // initialize the pushbutton player 2 pin as an input:
  pinMode(buttonPinP2, INPUT);
  // initialize the buzzer player 2 pin as an output:
  pinMode(buzzPinP2, OUTPUT);
  //initialise serial connection
  Serial.begin(9600);
  bool secondChance = false;
}

void loop() {
//  if (Serial.available() > 0) {
//    String command = Serial.readStringUntil('\n');
//
//    if (command == "answer_time") {
//        // read the state of the pushbutton value:
//        secondChance = true;
//        player = waitForButtonPress();
//        Serial.println(player);
//    }
//
//    if (command.substring(0, command.indexOf(',')) == "win"){
//      if(command.substring(command.indexOf(',') + 1) == "0"){
//        playerWin(0);
//      } else {
//        playerWin(1);
//      }
//      
//    }
//
//    if (command.substring(0, command.indexOf(',')) == "lose" and secondChance == true){
//      if(command.substring(command.indexOf(',') + 1) == "0"){
//        playerRetry(0);
//      } else {
//        playerRetry(1);
//      }
//      secondChance = false;
//    }
//
//    if (command.substring(0, command.indexOf(',')) == "lose" and secondChance == false){
//      if(command.substring(command.indexOf(',') + 1) == "0"){
//        playersFail(0);
//      } else {
//        playersFail(1);
//      }
//    }
//  }
  player = waitForButtonPress();
  delay(250);
  playerRetry(0);
  delay(250);
  playerFail(0);
  delay(2000);
}

int waitForButtonPress() {
  while (true) {
    if (digitalRead(buttonPinP1) == HIGH) {
      digitalWrite(ledPinGreenP1, HIGH);
      digitalWrite(ledPinRedP1, HIGH);
      tone(buzzPinP1, 150, 500);
      delay(500);
//      digitalWrite(ledPinRedP1, LOW);
//      digitalWrite(ledPinGreenP1, LOW);
      return 0; // 0 = player 1
    }
    if (digitalRead(buttonPinP2) == HIGH) {
      digitalWrite(ledPinGreenP2, HIGH);
      digitalWrite(ledPinRedP2, HIGH);
      tone(buzzPinP2, 300, 500);
      delay(500);
//      digitalWrite(ledPinGreenP2, LOW);
//      digitalWrite(ledPinRedP2, LOW);
      return 1; // 1 = player 2
    }
  }
}

void playerWin(int player) {
  if (player == 0){
    digitalWrite(ledPinRedP1, LOW);
    for (int i = 0; i < 5; i++) {
      digitalWrite(ledPinGreenP1, HIGH);
      tone(buzzPinP1, 150, 120);
      delay(140);
      digitalWrite(ledPinGreenP1, LOW);
      delay(50);
    }
  } else {
    digitalWrite(ledPinRedP2, LOW);
    for (int i = 0; i < 5; i++) {
      digitalWrite(ledPinGreenP2, HIGH);
      tone(buzzPinP2, 300, 120);
      delay(140);
      digitalWrite(ledPinGreenP2, LOW);
      delay(50);
    }
  }
}

void playerRetry(int player) {
  if (player == 0){
      digitalWrite(ledPinGreenP2, LOW);
      digitalWrite(ledPinGreenP1, HIGH);
      digitalWrite(ledPinRedP1, HIGH);
      tone(buzzPinP1, 300, 250);
      delay(260);
      tone(buzzPinP1, 300, 250);
      digitalWrite(ledPinRedP1, LOW);
      digitalWrite(ledPinGreenP1, LOW);
      delay(250);
      digitalWrite(ledPinGreenP1, HIGH);
      digitalWrite(ledPinRedP1, HIGH);
      delay(250);
      digitalWrite(ledPinGreenP1, LOW);
      digitalWrite(ledPinRedP1, LOW);
      delay(250);
      digitalWrite(ledPinGreenP1, HIGH);
      digitalWrite(ledPinRedP1, HIGH);
      delay(1000);
      digitalWrite(ledPinRedP2, LOW);
  }
  if (player == 1){
      digitalWrite(ledPinGreenP1, LOW);
      digitalWrite(ledPinGreenP2, HIGH);
      digitalWrite(ledPinRedP2, HIGH);
      tone(buzzPinP2, 300, 250);
      delay(260);
      tone(buzzPinP2, 300, 250);
      digitalWrite(ledPinRedP2, LOW);
      digitalWrite(ledPinGreenP2, LOW);
      delay(250);
      digitalWrite(ledPinGreenP2, HIGH);
      digitalWrite(ledPinRedP2, HIGH);
      delay(250);
      digitalWrite(ledPinGreenP2, LOW);
      digitalWrite(ledPinRedP2, LOW);
      delay(250);
      digitalWrite(ledPinGreenP2, HIGH);
      digitalWrite(ledPinRedP2, HIGH);
      delay(1000);
      digitalWrite(ledPinRedP1, LOW);
  }
}

void playerFail(int player) {
  if (player == 0){
      digitalWrite(ledPinGreenP1, LOW);
      delay(1500);
      digitalWrite(ledPinRedP1, LOW);
  }
  if (player == 1){
      digitalWrite(ledPinGreenP2, LOW);
      delay(1500);
      digitalWrite(ledPinRedP2, LOW);
  }
}
