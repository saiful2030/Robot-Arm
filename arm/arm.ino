#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo gripper;

// Posisi awal
int posBase = 90;
int posShoulder = 90;
int posElbow = 90;
int posGripper = 90;

String data = "";

const int SERVO_SPEED = 8;

void smoothMove(Servo &servo, int &currentPos, int targetPos)
{
  targetPos = constrain(targetPos, 0, 180);

  while (currentPos != targetPos)
  {
    if (currentPos < targetPos)
      currentPos++;
    else
      currentPos--;

    servo.write(currentPos);

    delay(SERVO_SPEED);
  }
}

void home() {
  posBase = 90;
  posShoulder = 90;
  posElbow = 90;
  posGripper = 90;

  smoothMove(base, posBase, 90);
  smoothMove(shoulder, posShoulder, 90);
  smoothMove(elbow, posElbow, 90);
  smoothMove(gripper, posGripper, 90);

  Serial.println("OK HOME");
}

void setup() {

  Serial.begin(9600);

  base.attach(3);
  shoulder.attach(5);
  elbow.attach(6);
  gripper.attach(9);

  home();

  Serial.println("READY");
}

void loop() {

  if (Serial.available()) {

    data = Serial.readStringUntil('\n');
    data.trim();

    if (data == "HOME") {
      home();
      return;
    }

    if (data == "STATUS") {
      Serial.print("B:");
      Serial.print(posBase);
      Serial.print(",S:");
      Serial.print(posShoulder);
      Serial.print(",E:");
      Serial.print(posElbow);
      Serial.print(",G:");
      Serial.println(posGripper);
      return;
    }

    if (data.length() < 2) return;

    char servo = toupper(data.charAt(0));
    int sudut = data.substring(1).toInt();

    sudut = constrain(sudut, 0, 180);

    switch (servo) {

      case 'B':
        smoothMove(base, posBase, sudut);
        Serial.println("OK");
        break;

      case 'S':
        smoothMove(shoulder, posShoulder, sudut);
        Serial.println("OK");
        break;

      case 'E':
        smoothMove(elbow, posElbow, sudut);
        Serial.println("OK");
        break;

      case 'G':
        smoothMove(gripper, posGripper, sudut);
        Serial.println("OK");
        break;

      default:
        Serial.println("ERROR");
        break;
    }
  }
}