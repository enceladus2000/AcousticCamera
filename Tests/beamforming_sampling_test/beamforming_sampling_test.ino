/* Records samples into samples[2][numSamples]
 * And sends the recorded waveforms on serial
 * So that the serial plotter can plot them on one graph 
 */

const int micPins[] = {A0, A1};
const int numMics = sizeof(micPins)/sizeof(int);

IntervalTimer samplingTimer;
const int numSamples = 1000;   //total number of samples in waveform
volatile int sampleCounter;   //must be volatile because is used in both main() and ISR
float samples[numMics][numSamples]; //stores 2 waveforms

const int ANALOG_READ_RESOLUTION = 12;
const int ANALOG_READ_AVERAGING = 1;
const int fs = 10000;    //sampling frequency

//to properly resolve one cycle of a waveform of frequency f, 
// numsamples >= fs / f or f >= fs / numSamples should be true

void setup() {
  Serial.begin(115200);
  //to (hopefully) ensure that the serial plotter plots two graphs
  for (int i = 0; i < 50; i++){
    Serial.println("100\t100"); 
    delay(15);
  }

  for (int i = 0; i < numMics; i++)
    pinMode(micPins[i], INPUT);

  analogReadResolution(ANALOG_READ_RESOLUTION);
  analogReadAveraging(ANALOG_READ_AVERAGING);  
}

void loop() {
  Serial.println("Beginning sampling...");
  //record start time of sample taking
  long beginTime = millis();
  samplingBegin();
  //wait for sampling to complete
  while (sampleCounter < numSamples);     //waiting for sampling to finish

  //now print all samples to serial port
  for (int i = 0; i < numSamples; i++){
    for (int m = 0; m < numMics; m++){
      Serial.print(samples[m][i]);
      Serial.print('\t');
    }
    Serial.println("");
  }
  
  Serial.print("Done sampling in ");
  Serial.print(millis() - beginTime);
  Serial.println("ms.");
  Serial.println("Waiting for 1 seconds");
  delay(1000);  
}

//record samples into samples[2][numSamples]
//should I do a noInterrupt in this callback?
void samplingCallback() {
  for (int m = 0; m < numMics; m++){
    samples[m][sampleCounter] = analogRead(micPins[m]);
  }

  sampleCounter++;
  if (sampleCounter >= numSamples) {
    samplingTimer.end();
  }
}

//initialise samplingTimer
void samplingBegin() {
  //initialise the sampling timer to an interval of 1000000/fs uS
  sampleCounter = 0;
  samplingTimer.begin(samplingCallback, 1000000 / fs);
}
