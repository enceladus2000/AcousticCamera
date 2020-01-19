/* Records samples into samples[2][numSamples]
 * And sends the recorded waveforms on serial
 * So that the serial plotter can plot them on one graph 
 */

const int micPin1 = A0;
const int micPin2 = A1;

IntervalTimer samplingTimer;
const int numSamples = 512;   //total number of samples in waveform
volatile int sampleCounter;   //must be volatile because is used in both main() and ISR
float samples[2][numSamples]; //stores 2 waveforms

const int ANALOG_READ_RESOLUTION = 10;
const int ANALOG_READ_AVERAGING = 16;
const int fs = 5000;    //sampling frequency

void setup() {
  Serial.begin(115200);
  //to (hopefully) ensure that the serial plotter plots two graphs
  for (int i = 0; i < 100; i++){
    Serial.println("100\t100"); 
    delay(15);
  }

  pinMode(micPin1, INPUT);
  pinMode(micPin2, INPUT);
  analogReadResolution(ANALOG_READ_RESOLUTION);
  analogReadAveraging(ANALOG_READ_AVERAGING);  
}

void loop() {
  Serial.println("Beginning sampling...");
  //record start time of sample taking
  long beginTime = millis();
  samplingBegin();
  //wait for sampling to complete
  while (sampleCounter < numSamples){
    //at least delay(1) is required for timer interrupt to work
    
  }
  
  for (int i = 0; i < numSamples; i++){
    Serial.print(samples[0][i]);
    Serial.print("\t");
    Serial.println(samples[1][i]);
  }
  
  Serial.print("Done sampling in ");
  Serial.print(millis() - beginTime);
  Serial.println("ms.");
  Serial.println("Waiting for 4 seconds");
  delay(4000);  
}

//record samples into samples[2][numSamples]
//should I do a noInterrupt in this callback?
void samplingCallback() {
  samples[0][sampleCounter] = analogRead(micPin1);
  samples[1][sampleCounter] = analogRead(micPin2);

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
