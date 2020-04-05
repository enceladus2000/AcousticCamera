# Running the Acoustic Camera Simulator

1. Enter this directory
2. run `python main.py`

# Code explanation

If all you're interested is simulations, you can largely ignore the `acousticsim.py` module. The relevant stuff is in `main.py`.

The main.py should consist of the following parts:

1. Initialising `mics` array.
2. Initialising a `Source` object.
3. Calling the Mic.generateWaveform() function for each mic instance.
4. Creating a scanArea, i.e a set of points (in 2D plane) that the algorithm will scan and output as an image.
5. The beamforming algorithm, which stores the acoustic 'image' in `bfImage[]`.
6. Data plotting - both raw waveforms and the `bfImage[]`.

# Tweaking code

You can 'play around' in this simulator by doing the following:

* Change mic arrangements: All the `Mic` instances should be stored in the list `mics`. The `Mic` constructor takes one argument; a tuple containing the x and y coordinate in metres.
* Change sound source position and frequency: The `Source` constructor takes these arguments. Currently only single source which generates a sine wave is supported. 
* Change the kind of beamforming algorithm: Currently a bare-bones simplistic delay and sum has been implemented.

