#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  1100 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);
  delay(10);
}

void loop() {
  if (Serial.available() > 0){
    String msg = Serial.readString();
    if (msg == "INIT"){
      initial();
      delay(500);
    }
    else if(msg == "A1"){
      moveToA1();
      delay(500);
    }
    else if(msg == "A2"){
      moveToA2();
      delay(500);
    }
    else if(msg == "A3"){
      moveToA3();
      delay(500);
    }
    else if(msg == "A4"){
      moveToA4();
      delay(500);
    }
    else if(msg == "A5"){
      moveToA5();
      delay(500);
    }
    else if(msg == "A6"){
      moveToA6();
      delay(500);
    }
    else if(msg == "A7"){
      moveToA7();
      delay(500);
    }
    else if(msg == "B1"){
      moveToB1();
      delay(500);
    }
    else if(msg == "B2"){
      moveToB2();
      delay(500);
    }
    else if(msg == "B3"){
      moveToB3();
      delay(500);
    }
    else if(msg == "B4"){
      moveToB4();
      delay(500);
    }
    else if(msg == "B5"){
      moveToB5();
      delay(500);
    }
    else if(msg == "B6"){
      moveToB6();
      delay(500);
    }
    else if(msg == "B7"){
      moveToB7();
      delay(500);
    }
    else if(msg == "C1"){
      moveToC1();
      delay(500);
    }
    else if(msg == "C2"){
      moveToC2();
      delay(500);
    }
    else if(msg == "C3"){
      moveToC3();
      delay(500);
    }
    else if(msg == "C4"){
      moveToC4();
      delay(500);
    }
    else if(msg == "C5"){
      moveToC5();
      delay(500);
    }
    else if(msg == "C6"){
      moveToC6();
      delay(500);
    }
    else if(msg == "C7"){
      moveToC7();
      delay(500);
    }
    else if(msg == "D1"){
      moveToD1();
      delay(500);
    }
    else if(msg == "D2"){
      moveToD2();
      delay(500);
    }
    else if(msg == "D3"){
      moveToD3();
      delay(500);
    }
    else if(msg == "D4"){
      moveToD4();
      delay(500);
    }
    else if(msg == "D5"){
      moveToD5();
      delay(500);
    }
    else if(msg == "D6"){
      moveToD6();
      delay(500);
    }
    else if(msg == "D7"){
      moveToD7();
      delay(500);
    }
    else if(msg == "E1"){
      moveToE1();
      delay(500);
    }
    else if(msg == "E2"){
      moveToE2();
      delay(500);
    }
    else if(msg == "E3"){
      moveToE3();
      delay(500);
    }
    else if(msg == "E4"){
      moveToE4();
      delay(500);
    }
    else if(msg == "E5"){
      moveToE5();
      delay(500);
    }
    else if(msg == "E6"){
      moveToE6();
      delay(500);
    }
    else if(msg == "E7"){
      moveToE7();
      delay(500);
    }
    else if(msg == "F1"){
      moveToF1();
      delay(500);
    }
    else if(msg == "F2"){
      moveToF2();
      delay(500);
    }
    else if(msg == "F3"){
      moveToF3();
      delay(500);
    }
    else if(msg == "F4"){
      moveToF4();
      delay(500);
    }
    else if(msg == "F5"){
      moveToF5();
      delay(500);
    }
    else if(msg == "F6"){
      moveToF6();
      delay(500);
    }
    else if(msg == "F7"){
      moveToF7();
      delay(500);
    }
    else if(msg == "G1"){
      moveToG1();
      delay(500);
    }
    else if(msg == "G2"){
      moveToG2();
      delay(500);
    }
    else if(msg == "G3"){
      moveToG3();
      delay(500);
    }
    else if(msg == "G4"){
      moveToG4();
      delay(500);
    }
    else if(msg == "G5"){
      moveToG5();
      delay(500);
    }
    else if(msg == "G6"){
      moveToG6();
      delay(500);
    }
    else if(msg == "G7"){
      moveToG7();
      delay(500);
    }
    else if(msg == "H1"){
      moveToH1();
      delay(500);
    }
    else if(msg == "H2"){
      moveToH2();
      delay(500);
    }
    else if(msg == "H3"){
      moveToH3();
      delay(500);
    }
    else if(msg == "H4"){
      moveToH4();
      delay(500);
    }
    else if(msg == "H5"){
      moveToH5();
      delay(500);
    }
    else if(msg == "H6"){
      moveToH6();
      delay(500);
    }
    else if(msg == "H7"){
      moveToH7();
      delay(500);
    }
    else if(msg == "KEP"){
      KEP();
      delay(500);
    }
    else if(msg == "THA"){
      THA();
      delay(500);
    }
    else if(msg == "OUT"){
      moveOut();
      delay(500);
    }
  }
}

void initial(){
  pwm.writeMicroseconds(1, 2500);
  delay(500);

  pwm.writeMicroseconds(2, 2400);
  delay(500);

  pwm.writeMicroseconds(0, 1950);
  delay(500);

  pwm.writeMicroseconds(3, 1500);
  delay(500);

  pwm.writeMicroseconds(4, 650);
  delay(500);

}

void KEP(){
  for (uint16_t servo_5 = 1100; servo_5 > 600; servo_5--) {
      pwm.writeMicroseconds(5, servo_5);
  }
  delay(500);
}

void THA(){
  for (uint16_t servo_5 = 600; servo_5 < 1100; servo_5++) {
      pwm.writeMicroseconds(5, servo_5);
  }
  delay(500);
}


void moveToA1() {
    pwm.writeMicroseconds(0, 2430);
    delay(500);

    pwm.writeMicroseconds(4, 900);
    delay(500);

    pwm.writeMicroseconds(2, 2400);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

    for (uint16_t microsec = 2500; microsec > 2100; microsec--) {
      pwm.writeMicroseconds(1, microsec);
      Serial.println(microsec);

    }
    delay(500);
}

void moveToA2() {
    pwm.writeMicroseconds(0, 2350);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2400);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2100; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToA3() {
    pwm.writeMicroseconds(0, 2290);
    delay(500);

    pwm.writeMicroseconds(4, 980);
    delay(500);

    pwm.writeMicroseconds(2, 2200);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2000; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);

}

void moveToA4() {
    pwm.writeMicroseconds(0, 2250);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 2100);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1950; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToA5() {
    pwm.writeMicroseconds(0, 2200);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 1950);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1850; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToA6() {
    pwm.writeMicroseconds(0, 2180);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 1700);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1700; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToA7() {
    pwm.writeMicroseconds(0, 2160);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 1500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1550; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);

}

void moveToB1() {
    pwm.writeMicroseconds(0, 2330);
    delay(500);

    pwm.writeMicroseconds(4, 900);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2150; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToB2() {
    pwm.writeMicroseconds(0, 2250);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2160; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToB3() {
    pwm.writeMicroseconds(0, 2210);
    delay(500);

    pwm.writeMicroseconds(4, 1150);
    delay(500);

    pwm.writeMicroseconds(2, 2400);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2110; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToB4() {
    pwm.writeMicroseconds(0, 2170);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2200);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2000; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToB5() {
    pwm.writeMicroseconds(0, 2150);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2050);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1920; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToB6() {
    pwm.writeMicroseconds(0, 2120);
    delay(500);

    pwm.writeMicroseconds(4, 1250);
    delay(500);

    pwm.writeMicroseconds(2, 1950);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1800; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToB7() {
    pwm.writeMicroseconds(0, 2120);
    delay(500);

    pwm.writeMicroseconds(4, 1300);
    delay(500);

    pwm.writeMicroseconds(2, 1750);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1700; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToC1() {
    pwm.writeMicroseconds(0, 2190);
    delay(500);

    pwm.writeMicroseconds(4, 830);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2160; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);

}

void moveToC2() {
    pwm.writeMicroseconds(0, 2140);
    delay(500);

    pwm.writeMicroseconds(4, 980);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToC3() {
    pwm.writeMicroseconds(0, 2120);
    delay(500);

    pwm.writeMicroseconds(4, 1070);
    delay(500);

    pwm.writeMicroseconds(2, 2400);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2130; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToC4() {
    pwm.writeMicroseconds(0, 2060);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2280);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2050; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}


void moveToC5() {
    pwm.writeMicroseconds(0, 2050);
    delay(500);

    pwm.writeMicroseconds(4, 1080);
    delay(500);

    pwm.writeMicroseconds(2, 2100);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1950; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToC6() {
    pwm.writeMicroseconds(0, 2030);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 1930);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1830; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToC7() {
    pwm.writeMicroseconds(0, 2030);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 1680);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1680; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}


void moveToD1() {
    pwm.writeMicroseconds(0, 1960);
    delay(500);

    pwm.writeMicroseconds(4, 730);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2160; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToD2() {
    pwm.writeMicroseconds(0, 1980);
    delay(500);

    pwm.writeMicroseconds(4, 890);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToD3() {
    pwm.writeMicroseconds(0, 1980);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToD4() {
    pwm.writeMicroseconds(0, 1970);
    delay(500);

    pwm.writeMicroseconds(4, 1080);
    delay(500);

    pwm.writeMicroseconds(2, 2300);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2050; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToD5() {
    pwm.writeMicroseconds(0, 1970);
    delay(500);

    pwm.writeMicroseconds(4, 1030);
    delay(500);

    pwm.writeMicroseconds(2, 2100);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1950; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToD6() {
    pwm.writeMicroseconds(0, 1955);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 1920);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1850; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToD7() {
    pwm.writeMicroseconds(0, 1970);
    delay(500);

    pwm.writeMicroseconds(4, 1120);
    delay(500);

    pwm.writeMicroseconds(2, 1700);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1680; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE1() {
    pwm.writeMicroseconds(0, 1820);
    delay(500);

    pwm.writeMicroseconds(4, 730);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2150; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE2() {
    pwm.writeMicroseconds(0, 1820);
    delay(500);

    pwm.writeMicroseconds(4, 950);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2180; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE3() {
    pwm.writeMicroseconds(0, 1870);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 2420);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2150; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE4() {
    pwm.writeMicroseconds(0, 1870);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 2250);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2050; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE5() {
    pwm.writeMicroseconds(0, 1880);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 2080);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1930; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE6() {
    pwm.writeMicroseconds(0, 1890);
    delay(500);

    pwm.writeMicroseconds(4, 1030);
    delay(500);

    pwm.writeMicroseconds(2, 1900);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1820; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToE7() {
    pwm.writeMicroseconds(0, 1895);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 1680);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1690; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF1() {
    pwm.writeMicroseconds(0, 1600);
    delay(500);

    pwm.writeMicroseconds(4, 800);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF2() {
    pwm.writeMicroseconds(0, 1700);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF3() {
    pwm.writeMicroseconds(0, 1730);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 2450);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2150; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF4() {
    pwm.writeMicroseconds(0, 1760);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2300);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2050; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF5() {
    pwm.writeMicroseconds(0, 1790);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2100);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1930; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF6() {
    pwm.writeMicroseconds(0, 1810);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 1900);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1830; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToF7() {
    pwm.writeMicroseconds(0, 1830);
    delay(500);

    pwm.writeMicroseconds(4, 1070);
    delay(500);

    pwm.writeMicroseconds(2, 1680);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1680; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG1() {
    pwm.writeMicroseconds(0, 1460);
    delay(500);

    pwm.writeMicroseconds(4, 900);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG2() {
    pwm.writeMicroseconds(0, 1550);
    delay(500);

    pwm.writeMicroseconds(4, 950);
    delay(500);

    pwm.writeMicroseconds(2, 2450);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2150; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG3() {
    pwm.writeMicroseconds(0, 1610);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 2300);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2070; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG4() {
    pwm.writeMicroseconds(0, 1650);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 2180);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2000; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG5() {
    pwm.writeMicroseconds(0, 1700);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 2060);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1920; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG6() {
    pwm.writeMicroseconds(0, 1720);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 1900);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1830; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToG7() {
    pwm.writeMicroseconds(0, 1760);
    delay(500);

    pwm.writeMicroseconds(4, 1100);
    delay(500);

    pwm.writeMicroseconds(2, 1550);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1620; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH1() {
    pwm.writeMicroseconds(0, 1330);
    delay(500);

    pwm.writeMicroseconds(4, 1030);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH2() {
    pwm.writeMicroseconds(0, 1450);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 2400);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2150; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH3() {
    pwm.writeMicroseconds(0, 1520);
    delay(500);

    pwm.writeMicroseconds(4, 1050);
    delay(500);

    pwm.writeMicroseconds(2, 2300);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2050; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH4() {
    pwm.writeMicroseconds(0, 1590);
    delay(500);

    pwm.writeMicroseconds(4, 920);
    delay(500);

    pwm.writeMicroseconds(2, 2050);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1950; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH5() {
    pwm.writeMicroseconds(0, 1610);
    delay(500);

    pwm.writeMicroseconds(4, 1000);
    delay(500);

    pwm.writeMicroseconds(2, 1950);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1880; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH6() {
    pwm.writeMicroseconds(0, 1655);
    delay(500);

    pwm.writeMicroseconds(4, 980);
    delay(500);

    pwm.writeMicroseconds(2, 1720);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1720; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}

void moveToH7() {
    pwm.writeMicroseconds(0, 1690);
    delay(500);

    pwm.writeMicroseconds(4, 1160);
    delay(500);

    pwm.writeMicroseconds(2, 1540);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 1600; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}


void moveOut(){
    pwm.writeMicroseconds(0, 900);
    delay(500);

    pwm.writeMicroseconds(4, 1030);
    delay(500);

    pwm.writeMicroseconds(2, 2500);
    delay(500);

    pwm.writeMicroseconds(3, 1500);
    delay(500);

  for (uint16_t microsec = 2500; microsec > 2200; microsec--) {
    pwm.writeMicroseconds(1, microsec);
    Serial.println(microsec);

  }
  delay(500);
}






