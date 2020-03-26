/* TESTED WITH FUNCGEN!!
 *  Records samples into samples[2][numSamples]
 *  shifts samples[0] to left by some amount
 * And sends the recorded waveforms on serial
 * So that the serial plotter can plot them on one graph 
 */

//number of samples to shift samples[0] to left
const int shiftValue = 25;

const int micPin1 = A0;
const int micPin2 = A1;

IntervalTimer samplingTimer;
const int numSamples = 550;   //total number of samples in waveform
volatile int sampleCounter;   //must be volatile because is used in both main() and ISR
int samples[2][numSamples]; //stores 2 waveforms

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
  //collect samples into matrix
  Serial.println("Beginning sampling...");
  //record start time of sample taking
  long beginTime = millis();
  samplingBegin();
  //wait for sampling to complete
  while (sampleCounter < numSamples);

  //sampling complete now process them
  shiftSamples(samples[0], numSamples, shiftValue);

  //print out shifted waveforms
  Serial.println("Shifted waveforms:");
  for (int i = 0; i < numSamples; i++){
    Serial.print(samples[0][i]);
    Serial.print("\t");
    Serial.println(samples[1][i]);
  }
  
  Serial.print("Done sampling in ");
  Serial.print(millis() - beginTime);
  Serial.println("ms.");
  Serial.println("Waiting for 4 seconds");
  delay(1500);  
}

//shifts a waveform array of size wsize
//to the left by delta samples
void shiftSamples(int *waveform, int wsize, int delta){
  int i = 0;
  while (i < wsize - delta){
    waveform[i] = waveform[i+delta];
    i++;
  }
  while (i < wsize){
    waveform[i] = 0;
    i++;
  }  
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
