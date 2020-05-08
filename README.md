# AcousticCamera

An acoustic camera is just like a regular optical camera, but is used to capture sound instead. Our project's aim is to create an open-source acoustic camera at significantly lower cost than commercial devices. 

## Basic Working

The acoustic camera consists of an array of mics. Sound from these mics are sampled and processed by a delay-and-sum beamforming algorithm. The result is a heatmap corresponding to intensities of sound from different points in space, thus resembling in a false colour image of 'sound'.

To learn more about the working of the acoustic camera, check out [this](https://github.com/DangerousTim/AcousticCamera/blob/master/docs/readme.md) list of resources.

## File descriptions

* [hardware/](https://github.com/DangerousTim/AcousticCamera/tree/master/hardware) consists of code for a Teensy 3.6 microcontroller, which was used in our first prototype.
* [simulations/](https://github.com/DangerousTim/AcousticCamera/tree/master/simulations) has a python program to simulate an acoustic camera implementation.
* [tools/](https://github.com/DangerousTim/AcousticCamera/tree/master/tools) has misc programs like serial port plotters and visualisers.
