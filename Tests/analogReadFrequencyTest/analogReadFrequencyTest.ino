//tests the analogread speed of the teensy
//is 431khz for read res 10bit and averaging 1 for a single input
const int inputs[] = {A0, A1};
const int numInputs = sizeof(inputs) / sizeof(int);

const int ANALOG_READ_RESOLUTION = 12;
const int ANALOG_READ_AVERAGING = 1;

const int numSamples = 400;
int samples[numInputs][numSamples];

void setup() {
  Serial.begin(115200);

  analogReadResolution(ANALOG_READ_RESOLUTION);
  analogReadAveraging(ANALOG_READ_AVERAGING); 
}

void loop() {
  //mark starting time
  unsigned long start = micros();
  //start taking samples as fast as possible
  for (int i = 0; i < numSamples; i++){
    //take a sample from each input pin
    for (int m = 0; m < numInputs; m++){
      samples[m][i] = analogRead(inputs[m]);
    }
  }
  //calculate the time taken for all of that sampling
  unsigned long delta = micros() - start;

  Serial.print("Time taken in uS = ");
  Serial.println(delta);
  Serial.print("Calculated sampling frequency in Hz = ");
  Serial.println(1000000.0 * numSamples / delta);

  delay(1500);
}
