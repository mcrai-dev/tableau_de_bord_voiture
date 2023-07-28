// const int sensorPin1 = A0;
// const int pinPower = 13;
// const int pin_marche_avant = 12;
// const int pin_marche_arriere = 11;
// const int pin_light = 10;
// String data = "";
// int pinPowerValue = 0;

// int i = 0;
// void setup() {

//   for (int index = 10; index < 14; index++) {
//     pinMode(i, INPUT_PULLUP);
//   }
//   pinMode(7, OUTPUT);
//   Serial.begin(9600);
//   // put your setup code here, to run once:
// }

// void loop() {
//   int n = analogRead(sensorPin1);
//   n = map(n, 0, 1023, 0, 220);

//   delay(10);
//   data = String(n + "#" + pinPower);

//   if (digitalRead(pinPower) == HIGH) {
//     if (pinPowerValue == 0) {
//       pinPowerValue = 1;
//     } else {
//       pinPowerValue = 0;
//     }
//   }
// digitalWrite(7, 0);
//   Serial.println(pinPowerValue);
// }

const int sensorPin1 = A0;
const int buttonPin = 2;
const int pinPower = 13;
const int pin_marche_avant = 12;
const int pin_marche_arriere = 11;
const int pin_light = 10;
int pinPowerValue = 0;
int buttonState = HIGH;
int lastButtonState = HIGH;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(7, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  buttonState = digitalRead(buttonPin);  // Lecture de l'état du bouton

  // Vérification si le bouton a été cliqué (transition de HIGH à LOW)
  if (buttonState == LOW && lastButtonState == HIGH) {
    if (pinPowerValue == 0) {
      pinPowerValue = 1;
    } else {
      pinPowerValue = 0;
    }
  }

  lastButtonState = buttonState;  // Mise à jour de l'état précédent du bouton

  int n = analogRead(sensorPin1);
  n = map(n, 0, 1023, 0, 220);

  delay(10);
  pinPowerValue = n;

  digitalWrite(7, LOW);
  Serial.println(n);
}
