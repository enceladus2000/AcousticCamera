#define numLines 50

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.println("#waveform");
  for (int i = 0; i < numLines; i++){
    Serial.print((float)random(1023) / 4);
    Serial.print('\t');
    Serial.println((float)random(1023) / 4);
  }
  Serial.println("#!waveform");

  Serial.println("#bfimage");
  for (int i = 0; i < 20; i++){
    Serial.println((float) random(1023) / 4);
  }
  Serial.println("#!bfimage");
  Serial.println("Waiting for 1 second...");
  delay(1000);
}
