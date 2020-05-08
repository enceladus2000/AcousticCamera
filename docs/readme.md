# Resources

If you are unfamiliar with an acoustic camera and how it functions, first check out [this](https://www.youtube.com/watch?v=ewYWXS_Jjew) video.

### Acoustic Beamforming

Acoustic beamforming refers to the broad range of signal processing techniques used with arrays of microphones to extract directional information from sound. In other words, it is used to achieve _sound localisation_, i.e. to locate sources of sound, and this is fundamentally how acoustic cameras work.

### Delay-And-Sum Beamforming

Time domain delay-and-sum beamforming (DSBF) is the simplest method, which is what we have implement currently in our simulation. For a light introduction, check out the following:

* <http://www.labbookpages.co.uk/audio/beamforming/delaySum.html>
* [Paper on 8 mic acoustic camera](https://drive.google.com/open?id=1sBlHpNIhVz643Zun4pMwJ3veJLWjnkmI) See section 3.1, pg34

Other acoustic camera projects using DSBF (Delay-and-Sum BeamForming):

* [64 mic array](https://drive.google.com/open?id=1922aiDXqvHQdEGeUMkxZuLKnRbTwEwf6) 
* [Design and build of a planar acoustic camera](https://drive.google.com/open?id=1rt9U72PY10CY26k4ek_eipbRq3nJiIhc)

### Other sound localisation algorithms

* MUSIC
* SRP-PHAT

