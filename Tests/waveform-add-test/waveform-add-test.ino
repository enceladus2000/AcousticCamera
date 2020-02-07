/* TESTED WITH FUNCGEN! implement adding into separate function
 *  Records samples into samples[2][numSamples]
 *  adds them into another waveform array
 *  and calculates the power
 * And sends the recorded waveforms on serial
 * So that the serial plotter can plot them on one graph 
 */

const int micPin1 = A0;
const int micPin2 = A1;

IntervalTimer samplingTimer;
const int numSamples = 512;   //total number of samples in waveform
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
  Serial.println("Beginning sampling...");
  //record start time of sample taking
  long beginTime = millis();
  samplingBegin();
  //wait for sampling to complete
  while (sampleCounter < numSamples);

  //now do some signal processing

  //normalise them ie take out the DC component
  centerWaveform(samples[0], numSamples);
  centerWaveform(samples[1], numSamples);

  long samplesSum[numSamples];
  zeroArray(samplesSum, numSamples);
  //addWaveforms(samplesSum, 2, numSamples, (int**)samples);

  //function might not be working because it doens't like double pointer
  for (int i = 0; i < numSamples; i++){
    for (int m = 0; m < 2; m++){
      samplesSum[i] += samples[m][i];
    }
  }
  for (int i = 0; i < numSamples; i++){
    Serial.print(samples[0][i]);
    Serial.print("\t");
    Serial.print(samples[1][i]);
    Serial.print("\t");\
    Serial.println(samplesSum[i]);
  }
  
  Serial.print("Done sampling and processing in num");
  Serial.print(millis() - beginTime);
  Serial.println("ms.");

  Serial.print("Intensity of summed signal = num");
  Serial.println(calcPower(samplesSum, numSamples));
  
  Serial.println("Waiting for num4 seconds");
  delay(4000);  
}

//calculates power of waveform
float calcPower(long *waveform, int wsize){
  float result = 0;
  for (int i = 0; i < wsize; i++){
    result += sq(waveform[i]);
  }
  result /= wsize;
  return result;
}

//take an matrix of waveforms[numwaves][wsize]
//sum all the waves into sum[wsize] 
//sum[] is assumed to be zeroed
void addWaveforms(long *sum, int numwaves, int wsize, int **waveforms){
  for (int i = 0; i < wsize; i++){
    for (int j = 0; j < numwaves; j++){
      sum[i] += waveforms[j][i];
    }    
  }
}

void centerWaveform(int *waveform, int wsize){
  long average = 0;
  //calculate mean
  for (int i = 0; i < wsize; i++){
    average += waveform[i];
  }
  average /= numSamples;

  //subtract mean from each value in waveform[]
  for (int i = 0; i < wsize; i++){
    waveform[i] -= average;
  }
}

//set all values in array to 0
void zeroArray(long *a, int asize){
  for (int i = 0; i < asize; i++){
    a[i] = 0;
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
