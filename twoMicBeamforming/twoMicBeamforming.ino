/*
   do beamforming on a linear scan area using two mics
   beamforming results are stored as intensity values in float array
   which is then sent on serial monitor to be plotted as a heatmap
*/
//mic1 is on the same side as scan area element 1
const int micPin1 = A0;
const int micPin2 = A1;

const int numPoints = 40;       //number of points in scan area
//all distances in meters
const float pointStep = 0.10;       //distance between consecutive scan points
const float scanDist = 2.00;       //distance of scanning area from mics
const float micDist = 0.28;          //distance between two mics
//angle subtended by scan area = 2 * atan((numPoints/2)*pointStep / scanDist)
float scanArea[numPoints];

const int fs = 20000;      //sampling freq
const int c = 343;        //speed of sound (m/s)

int Delays[2][numPoints];
int intensities[numPoints]; //array that stores final data

IntervalTimer samplingTimer;
const int numSamples = 500;   //total number of samples in waveform
int sampleCounter;
int samples[2][numSamples]; //stores 2 waveforms
//to properly resolve one cycle of a waveform of frequency f, 
// numsamples >= fs / f or f >= fs / numSamples should be true

const int ANALOG_READ_RESOLUTION = 10;
const int ANALOG_READ_AVERAGING = 1;

void setup() {
  Serial.begin(115200);
  delay(1000);
  calcDelays();
  Serial.println("unnormalised delays: ");
  printDelays();
  normaliseDelays();
  Serial.println("normalised delays");
  printDelays();

  analogReadResolution(ANALOG_READ_RESOLUTION);
  analogReadAveraging(ANALOG_READ_AVERAGING);
}

void loop() {
//  Serial.println("Beginning sampling...");
//  samplingBegin();
//  while (sampleCounter < numSamples);   //waiting for sampling to finish

  //now process the signals
  for (int m = 0; m < 2; m++)
    centerWaveform(samples[m], numSamples);

  //update scanArea array with the results of beamforming
  Beamforming();
  for (int p = 0; p < numPoints; p++){
    //Serialprint
  }
}

//please check this code for logical errors
void Beamforming() {
  for (int p = 0; p < numPoints; p++){
    int bfsigsize = numSamples - max(Delays[0][p], Delays[1][p]);
    long bfSignal[bfsigsize];  //beamformed signal

    for (int i = 0; i < bfsigsize; i++){
      bfSignal[i] = samples[0][i+Delays[0][p]] + samples[1][i+Delays[1][p]];
    }
    scanArea[p] = calcPower(bfSignal, bfsigsize);
  }  
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

//removes dc component of waveform
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

//for debugging
void printDelays(){
  for (int p = 0; p < numPoints; p++){
    for (int m = 0; m < 2; m++){
      Serial.print(Delays[m][p]);
      Serial.print('\t');
    }
    Serial.println("");
  }
}

//fill the Delays[][] matrix
void calcDelays() {
  for (int i = 0; i < numPoints; i++) {
    Delays[0][i]
      = round(sqrt(sq(pointStep * (numPoints / 2 - i) - micDist / 2) + sq(micDist)) * (float) fs / c);
    Delays[1][i]
      = round(sqrt(sq(pointStep * (numPoints / 2 - i) + micDist / 2) + sq(micDist)) * (float) fs / c);
  }
}

/*  calcDelays will calculate the time taken for sound to travel 
 *  from each point to each mic. We need to convert those values 
 *  to relative values, this is done by normaliseDelays()
 */
void normaliseDelays(){
  for (int p = 0; p < numPoints; p++){
    int minDelayPointp = min(Delays[0][p], Delays[1][p]);
    for (int m = 0; m < 2; m++){
      Delays[m][p] -= minDelayPointp;
    }
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
