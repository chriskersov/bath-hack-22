const int buttonPinP1 = 3;     // the number of the pushbutton pin for player 1
const int ledPinGreenP1 =  5;  // the number of the green LED pin for player 1
const int ledPinRedP1 = 2;     // the number of the red LED pin for player 1
const int buzzPinP1 =  4;      // the number of the buzzer pin for player 1
const int buttonPinP2 = 11;      // the number of the pushbutton pin for player 2
const int ledPinGreenP2=  10;    // the number of the green LED pin for player 2
const int ledPinRedP2 = 13;      // the number of the red LED pin for player 2
const int buzzPinP2 =  12;       // the number of the buzzer pin for player 2

int player = 0;
bool secondChance = false;

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
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "answer_time") {
        // read the state of the pushbutton value:
        secondChance = true;
        player = waitForButtonPress();
        Serial.println(player);
        while (Serial.available() > 0) {
          Serial.read();
        }
    }

    if (command.substring(0, command.indexOf(',')) == "win"){
      if(command.substring(command.indexOf(',') + 1) == "0"){
        playerWin(0);
        while (Serial.available() > 0) {
          Serial.read();
        }
      } else {
        playerWin(1);
        while (Serial.available() > 0) {
          Serial.read();
        }
      }
      
    }

    if (command.substring(0, command.indexOf(',')) == "lose" && secondChance == true){
      if(command.substring(command.indexOf(',') + 1) == "1"){
        playerRetry(0);
        while (Serial.available() > 0) {
          Serial.read();
        }
      } else {
        playerRetry(1);
        while (Serial.available() > 0) {
          Serial.read();
        }
      }
      secondChance = false;
    }

    if (command.substring(0, command.indexOf(',')) == "lose" && secondChance == false){
      if(command.substring(command.indexOf(',') + 1) == "0"){
        playersFail(0);
        while (Serial.available() > 0) {
          Serial.read();
        }
      } else {
        playersFail(1);
        while (Serial.available() > 0) {
          Serial.read();
        }
      }
    }
  }
//  player = waitForButtonPress();
//  playerWin(player);
}

int waitForButtonPress() {
  while (true) {
    if (digitalRead(buttonPinP1) == HIGH) {
      digitalWrite(ledPinGreenP1, HIGH);
      digitalWrite(ledPinRedP1, HIGH);
      tone(buzzPinP1, 150, 500);
      delay(500);
      return 0; // 0 = player 1
    }
    if (digitalRead(buttonPinP2) == HIGH) {
      digitalWrite(ledPinGreenP2, HIGH);
      digitalWrite(ledPinRedP2, HIGH);
      tone(buzzPinP2, 300, 500);
      delay(500);
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

void playersFail(int player) {
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
