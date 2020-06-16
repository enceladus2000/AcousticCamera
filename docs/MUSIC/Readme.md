# MUSIC algorithm for the Direction of Arrival estimation for multiple sources.
MUSIC stands for Multiple signal classication
The  basic  idea  of  DOA  estimation  by  MUSIC algorithm  is  that  the  narrowband  signal  captured  by  microphone  array  gives  a covariance matrix of a rank equal to number of signal sources and the matrix formed "R" can be decomposed into two orthogonal subspaces namely signal subspace and noise subspace.
The signal subspace is represented by Eigen Vectors corresponding to high power  Eigen Values and  noise  subspace  is  represented  by  Eigen  Vectors  corresponding  low  power  Eigen Values. 
The signal subspace corresponds to array manifolds and thus the dot product of  array  manifold  matrix A(  )  and  noise  subspace  will  be  minimum(zero)  in  the direction of true DOA.

For an introduction to MUSIC check out the following:

https://www.ripublication.com/ijeer17/ijeerv9n4_09.pdf. </br>
https://pdfs.semanticscholar.org/5ff7/806b44e60d41c21429e1ad2755d72bba41d7.pdf.

### The above simulator has been made for 4 mic linear array configuration with 2 sound sources and gaussian noise, the number of sound sources can be increased provided the number of mic elements are always greater than the number of sound sources.

<img src = "https://github.com/aadhar218/AcousticCamera/blob/master/docs/MUSIC/MUSIC.png" width = 500>

The peak in the figure gives the direction of arrival.
