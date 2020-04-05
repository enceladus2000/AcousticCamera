# Running the Acoustic Camera Simulator

1. Make sure you have matplotlib and numpy installed.
2. Enter this directory.
3. On command line, run using `python main.py`.

# Code explanation

This is a simulation program to test out implementations of a microphone-array acoustic camera.

The main.py should consist of the following parts:

1. Creating a `scanArea[]`, i.e a set of points (in 2D plane) that the algorithm will scan and output as an image.
2. Definition of `mics`: A list of `Mic` objects.
3. Initialising a `Source` object.
4. Calling the `Mic.generateWaveform()` function for each mic in `mics`.
5. The beamforming algorithm, which renders the acoustic 'image' and stores it in `bfImage[]`.
6. Data plotting. 

# Tweaking code

You can 'play around' in this simulator by doing the following:

* **Change mic arrangements:** All the `Mic` instances should be stored in the list `mics`. The `Mic` constructor takes one argument - a tuple containing the x and y coordinate in metres. 
* **Change sound source position and frequency:** The `Source` constructor takes these arguments. Currently only single source which generates a sine wave is supported. 
* **Change the kind of beamforming algorithm:** Currently a bare-bones simplistic delay-and-sum algorithm has been implemented.

