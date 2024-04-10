#define relay1 5
#define relay2 6
#define relay3 7
#define relay4 8

int data;

void setup() {
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(relay1, OUTPUT); //for ESP8266
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  
  digitalWrite(relay1, LOW);
  digitalWrite(relay2, LOW);
  digitalWrite(relay3, LOW);
  digitalWrite(relay4, LOW);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("Hi!, I am Arduino");
}

void loop() {
  while (Serial.available()) {
    data = Serial.read();
    //    data = Serial.parseInt();
    Serial.println(data);
  }
  if (data == '0') {
    digitalWrite(relay2, HIGH);
    digitalWrite(relay1, LOW);
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else if (data == '1') {
    digitalWrite(relay2, LOW);
    digitalWrite(relay1, HIGH);
    digitalWrite(LED_BUILTIN, LOW);
  }
  else if (data == '2') {
    digitalWrite(relay2, LOW);
    digitalWrite(relay1, LOW);
  }
}
