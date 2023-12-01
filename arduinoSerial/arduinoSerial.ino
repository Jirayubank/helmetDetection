int data;

void setup() {
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(LED_BUILTIN, OUTPUT); //make the LED pin (13) as output
  digitalWrite (LED_BUILTIN, LOW);

  Serial.println("Hi!, I am Arduino");
}

void loop() {
  while (Serial.available()) {
    data = Serial.read();
  }
//  Serial.println(data);
  if (data == '1')
    digitalWrite (LED_BUILTIN, HIGH);

  else if (data == '0')
    digitalWrite (LED_BUILTIN, LOW);

}
