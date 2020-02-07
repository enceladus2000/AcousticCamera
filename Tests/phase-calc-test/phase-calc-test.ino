/* TESTED WITH FUNCGEN! 
  takes 2 waveforms of same freqency, 1 lagging by some phase
  code performs beamforming algorithm at several times
  and calculates the phase difference of the 2 waveforms
*/
const int signalFreq = 100;

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
  delay(500);

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

  //doing a beamform at all possible non repeating deltas
  //ie calculating intensity when 2 signals are added with all possible phases
  
  const int hspr = 26;   //half of samples per revolution plus 1
  float bfReadings[hspr];
  for (int i = 0; i < hspr; i++){
    bfReadings[i] = beamformAtDelta(i);
  }

  //find the index of brReadings with highest value
  //this corresponds to the phase angle
  int deltaPeak = 0;
  for (int i = 1; i < hspr; i++){
    if (bfReadings[i] > bfReadings[deltaPeak]){
      deltaPeak = i;
    }
  }

  Serial.println("Result of beamform from 0 to 25 delta: ");
  for (int i = 0; i < 25; i++) {
    Serial.println(bfReadings[i]);
  }
  Serial.print("deltaPeak = ");
  Serial.println(deltaPeak);
  Serial.print("Corresponding phase = ");
  Serial.println((float) deltaPeak / hspr * 180);
  Serial.print("Error in calculating phase = ");
  Serial.println((float) 1 / hspr * 180);

  Serial.println("Waiting for num1.5 seconds");
  delay(1500);
}
//wow i wrote all this code fuck

float beamformAtDelta(int delta) {
  int sumSize = numSamples - delta;
  long *sum = (long*) calloc(sumSize, sizeof(long));
  
  //calloc inits all values to 0 so zeroArray not required
  for (int i = 0; i < sumSize; i++) {
    sum[i] = samples[0][i] + samples[1][i + delta];
  }
  float result = calcPower(sum, sumSize);
  free(sum);
  return result;
}

//calculates power of waveform
float calcPower(long *waveform, int wsize) {
  float result = 0;
  for (int i = 0; i < wsize; i++) {
    result += sq(waveform[i]);
  }
  result /= wsize;
  return result;
}

//take an matrix of waveforms[numwaves][wsize]
//sum all the waves into sum[wsize]
//sum[] is assumed to be zeroed
void addWaveforms(long *sum, int numwaves, int wsize, int **waveforms) {
  for (int i = 0; i < wsize; i++) {
    for (int j = 0; j < numwaves; j++) {
      sum[i] += waveforms[j][i];
    }
  }
}

void centerWaveform(int *waveform, int wsize) {
  long average = 0;
  //calculate mean
  for (int i = 0; i < wsize; i++) {
    average += waveform[i];
  }
  average /= numSamples;

  //subtract mean from each value in waveform[]
  for (int i = 0; i < wsize; i++) {
    waveform[i] -= average;
  }
}

//set all values in array to 0
void zeroArray(long *a, int asize) {
  for (int i = 0; i < asize; i++) {
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
