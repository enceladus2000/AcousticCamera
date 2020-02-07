/*
   do beamforming on a linear scan area using two mics
   beamforming results are stored as intensity values in float array
   which is then sent on serial monitor to be plotted as a heatmap
*/
//mic1 is on the same side as scan area element 1
const int micPins[] = {A0, A1};
const int numMics = sizeof(micPins) / sizeof(int);    //at least in this sketch, numMics is limited to 2

const int numPoints = 41;       //number of points in scan area, should be an odd number
//all distances in meters
const float pointStep = 0.05;       //distance between consecutive scan points
const float scanDist = 0.30;       //distance of scanning area from mics
const float micDist = 0.39;          //distance between two mics
//angle subtended by scan area = 2 * atan((numPoints/2)*pointStep / scanDist)
float scanArea[numPoints];          //stores results of beamforming

const int fs = 30000;      //sampling freq
const int c = 343;        //speed of sound (m/s)

//Delays should be (and are from testing) symmetrical
//floats are necessary so as not to lose information during normalising.
//floats might also be useful for upsampling tests
float Delays[2][numPoints];   //stores delay for each mic and point in scan area
int intensities[numPoints]; //array that stores final data

IntervalTimer samplingTimer;
const int numSamples = 600;   //total number of samples in waveform
volatile int sampleCounter;   //must be volatile because is used in both main() and ISR
float samples[numMics][numSamples]; //stores 2 waveforms
//to properly resolve one cycle of a waveform of frequency f,
// numsamples >= fs / f or f >= fs / numSamples should be true

const int ANALOG_READ_RESOLUTION = 10;
const int ANALOG_READ_AVERAGING = 1;

void setup() {
  Serial.begin(115200);
  delay(1000);
  calcDelays();
  Serial.println("normalised delays");
  printDelays();

  analogReadResolution(ANALOG_READ_RESOLUTION);
  analogReadAveraging(ANALOG_READ_AVERAGING);
}

void loop() {
  //Serial.println("Beginning sampling...");
  samplingBegin();
  while (sampleCounter < numSamples);   //waiting for sampling to finish
  //Serial.println("Done sampling!");

  //now process the signals
  //remove the dc component
  for (int m = 0; m < 2; m++)
    centerWaveform(samples[m], numSamples);

  //update scanArea array with the results of beamforming
  Beamforming();

  printWaveforms();
  printBFI();

  Serial.println("Pausing for 1s...");
  delay(700);
}

void printWaveforms() {
  float bfweights[2]; 

  //calculate beamforming weights from waveform power
  for (int m = 0; m < 2; m++) {
    bfweights[m] = sqrt(calcPower(samples[m], numSamples));
  }

  Serial.println("#waveform");
  for (int i = 0; i < numSamples; i++) {
    Serial.print(samples[0][i] / bfweights[0]);
    Serial.print('\t');
    Serial.println(samples[1][i] / bfweights[1]);
  }
  Serial.println("#!waveform");
}

void printBFI() {
  Serial.println("#bfimage");
  for (int p = 0; p < numPoints; p++) {
    Serial.println(scanArea[p], 10);
  }
  Serial.println("#!bfimage");
}

//please check this code for logical errors
void Beamforming() {
  for (int p = 0; p < numPoints; p++) {
    int intdly[2];    //rounded int delays for array manipulation
    float bfweights[2]; //weights for each mic when beamforming

    //calculate beamforming weights from waveform power
    for (int m = 0; m < 2; m++) {
      bfweights[m] = sqrt(calcPower(samples[m], numSamples));
      intdly[m] = round(Delays[m][p]);
    }
    int bfsigsize = numSamples - max(intdly[0], intdly[1]);   //size of beamformed waveform
    float bfSignal[bfsigsize];  //beamformed signal (sum of shifted waveforms)

    //add shifted waveforms together with bfweights into bfSignal
    for (int i = 0; i < bfsigsize; i++) {
      bfSignal[i] = 0;
      for (int m = 0; m < 2; m++) {
        bfSignal[i] += samples[m][i + intdly[m]] / bfweights[m];
      }
    }
    scanArea[p] = calcPower(bfSignal, bfsigsize) * avg(bfweights[0], bfweights[1]);
  }
}

//calculates power of waveform
float calcPower(float *waveform, int wsize) {
  float result = 0;
  for (int i = 0; i < wsize; i++) {
    result += sq(waveform[i]);
  }
  result /= wsize;
  return result;
}

//removes dc component of waveform
void centerWaveform(float *waveform, int wsize) {
  float average = 0;
  //calculate mean
  for (int i = 0; i < wsize; i++) {
    average += waveform[i];
  }
  average /= wsize;

  //subtract mean from each value in waveform[]
  for (int i = 0; i < wsize; i++) {
    waveform[i] -= average;
  }
}

//for debugging
void printDelays() {
  for (int p = 0; p < numPoints; p++) {
    for (int m = 0; m < 2; m++) {
      Serial.print(Delays[m][p]);
      Serial.print('\t');
    }
    Serial.println("");
  }
}

//fill the Delays[][] matrix using calculated sample delay values
//and also normalise the matrix by converting to relative values
void calcDelays() {
  for (int i = 0; i < numPoints; i++) {
    //calculate sample delay using geometry
    float d1
      = sqrt(sq(pointStep * (numPoints / 2 - i) - micDist / 2) + sq(micDist)) * (float) fs / c;
    float d2
      = sqrt(sq(pointStep * (numPoints / 2 - i) + micDist / 2) + sq(micDist)) * (float) fs / c;
    //normalise the delay and round into integers
    float min_d = min(d1, d2);
    Delays[0][i] = (d1 - min_d);
    Delays[1][i] = (d2 - min_d);
  }
}

float avg(float a, float b) {
  return (a + b) / 2;
}

//record samples into samples[2][numSamples]
//should I do a noInterrupt in this callback?
//callback takes 4-5uS
void samplingCallback() {
  for (int m = 0; m < numMics; m++) {
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
