/* Records samples into samples[2][numSamples]
 * centralises and normalises the waveforms
 * HOW TO NORMALISE A WAVEFORM? 
 * 
 *
 * And sends the resultant waveforms on serial
 * So that the serial plotter can plot them on one graph 
 */

const int micPins[] = {A0, A1};
const int numMics = sizeof(micPins)/sizeof(int);

IntervalTimer samplingTimer;
const int numSamples = 600;   //total number of samples in waveform
volatile int sampleCounter;   //must be volatile because is used in both main() and ISR
float samples[numMics][numSamples]; //stores 2 waveforms

const int ANALOG_READ_RESOLUTION = 10;
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

  float p1 = calcPower(samples[0], numSamples);
  p1 = sqrt(p1);
  float p2 = calcPower(samples[1], numSamples);
  p2 = sqrt(p2);
  
  for (int m = 0; m < numMics; m++){
    centerWaveform(samples[m], numSamples);
    normaliseWaveform(samples[m], numSamples);
  }

  //now print all samples to serial port
  for (int i = 0; i < numSamples; i++){
    for (int m = 0; m < numMics; m++){
      Serial.print(samples[m][i]);
      Serial.print('\t');
    }
    Serial.println("");
  }
  
  Serial.print("Power of each waveform: num");
  Serial.print(p1); Serial.print("\t num");
  Serial.println(p2);
  
  Serial.println("Waiting for 1 seconds");
  delay(1000);  
}

//takes a previously centralised waveform
//and divides each sample by the total power of the waveform
void normaliseWaveform(float *waveform, int wsize){
  float wpower = calcPower(waveform, wsize);
  float factor = sqrt(wpower) / wsize ;
  for (int i = 0; i < wsize; i++){
    waveform[i] /= factor;
  }
}

//calculates power of waveform
float calcPower(float *waveform, int wsize){
  float result = 0;
  for (int i = 0; i < wsize; i++){
    result += sq(waveform[i]);
  }
  result /= wsize;
  return result;
}

//removes dc component of waveform
void centerWaveform(float *waveform, int wsize){
  float average = 0;
  //calculate mean
  for (int i = 0; i < wsize; i++){
    average += waveform[i];
  }
  average /= wsize;

  //subtract mean from each value in waveform[]
  for (int i = 0; i < wsize; i++){
    waveform[i] -= average;
  }
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
