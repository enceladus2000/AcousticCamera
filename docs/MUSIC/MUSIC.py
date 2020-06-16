# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt

d=0.5 # spacing between mics
M=4 # no. of mics
N= 2**12 # sampling size
theta_1 =50 # incident angle of source
theta_2=80
  #steering vector

# response from test source 1
a_1 = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.cos(np.deg2rad(theta_1)))

# Array response vectors of test source 2
a_2 = np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.cos(np.deg2rad(theta_2)))

soi = np.random.normal(0,1,N)  # Signal of Interest
soi_matrix  = ( np.outer( soi, a_1) + np.outer( soi, a_2)).T 

# Generate multichannel uncorrelated noise
noise = np.random.normal(0,np.sqrt(10**-1),(M,N))

# Create received signal array
rec_signal = soi_matrix + noise                                                                 # a sample signal is created 

# correlational spectral matrix from the signal is created 
def cor_spect_estimate(X):
  N=np.size(X,0)
  M= np.size(X,1)
  R= np.zeros((M,M) ,dtype=complex)
  X= X.T
  R =np.dot(X,X.conj().T)
  R = np.divide(R,N)
  return R

R= cor_spect_estimate(rec_signal.T)

# scanning area
def forward_backward_avg(R):                                                              # when there are more than 1 sources forward_backaerd_avg is done
    """
        Calculates the forward-backward averaging of the input correlation matrix
        
    Parameters:
    -----------
        :param R : Spatial correlation matrix
        :type  R : M x M complex numpy array, M is the number of antenna elements.        
            
    Return values:
    -------------
    
        :return R_fb : Forward-backward averaged correlation matrix
        :rtype R_fb: M x M complex numpy array           
        
        :return -1, -1: Input spatial correlation matrix is not quadratic
            
    """          
    # --> Input check
    if np.size(R, 0) != np.size(R, 1):
        print("ERROR: Correlation matrix is not quadratic")
        return -1, -1 
    
    # --> Calculation
    M = np.size(R, 0)  # Number of antenna elements
    R = np.matrix(R)

    # Create exchange matrix
    J = np.eye(M)
    J = np.fliplr(J) 
    J = np.matrix(J)
    
    R_fb = 0.5 * (R + J*np.conjugate(R)*J)

    return np.array(R_fb)

R_fb = forward_backward_avg(R)

def ula_scan(array_type,thetas):
  M = np.size(array_alignment, 0)  # Number of antenna elements    
  scanning_vectors = np.zeros((M, np.size(thetas)), dtype=complex)
  for i in range(np.size(thetas)):    
      scanning_vectors[:, i] = np.exp(array_alignment*1j*2*np.pi*np.cos(np.radians(thetas[i]))) # Scanning vector      
        
  return scanning_vectors

array_alignment = np.arange(0, M, 1)* d
incident_angles= np.arange(0,181,1)
scanning_vector = ula_scan(array_alignment,incident_angles)
# Music (Mulitple signal classification algorithm for identification of multiple sources)
def MUSIC(R_fb,scanning_vector,signal_dimension=2):
  M = np.size(R_fb,0)
  N1,V= lin.eig(R_fb)
  eig_array=[]
  Power = np.zeros(np.size(scanning_vector, 1),dtype=complex)
  for i in range(M):
    eig_array.append([np.abs(N1[i]),V[:,i]])
  eig_array = sorted(eig_array, key=lambda eig_array: eig_array[0], reverse=False)
   # Generate noise subspace matrix
  noise_dimension = M - signal_dimension    
  E = np.zeros((M,noise_dimension),dtype=complex)                                                            # sorted in ascending order 
  for i in range(noise_dimension):     
       E[:,i] = eig_array[i][1]     
        
  E = np.matrix(E) 
  theta_index=0
  
  for i in range(np.size(scanning_vector, 1)):             
        S_theta_ = scanning_vector[:, i]
        S_theta_  = np.matrix(S_theta_).getT() 
        Power[theta_index]=  1/np.abs(S_theta_.getH()*(E*E.getH())*S_theta_)     # geth return complex conjugate transpose
        theta_index += 1
         
  return Power

Power=MUSIC(R_fb,scanning_vector,signal_dimension=2)                                 # signal dimension depends on the number of sources
def alias_border_calc(d):
    """
        Calculate the angle borders of the aliasing region for ULA antenna systems
    Parameters:
    -----------        
        :param d: distance between antenna elements [lambda]
        :type d: float
    
    Return values:
    --------------
        :return anlge_list : Angle borders of the unambious region
        :rtype anlge_list: List with two elements
    """
    theta_alias_min = np.rad2deg(np.arccos(1/(2*d)))
    theta_alias_max = np.rad2deg(np.arccos(1/d -1))
    return (theta_alias_min,theta_alias_max)

def DOA_plot(DOA_data, incident_angles, log_scale_min=None, alias_highlight=True, d=0.5, axes=None):
    
    DOA_data = np.divide(np.abs(DOA_data),np.max(np.abs(DOA_data))) # normalization
    if(log_scale_min != None):        
        DOA_data = 10*np.log10(DOA_data)                
        theta_index = 0        
        for theta in incident_angles:                    
            if DOA_data[theta_index] < log_scale_min:
                DOA_data[theta_index] = log_scale_min
            theta_index += 1                     
        
    if axes is None:
        fig = plt.figure()
        axes  = fig.add_subplot(111)
    
    #Plot DOA results  
    axes.plot(incident_angles,DOA_data)    
    axes.set_title('Direction of Arrival estimation ',fontsize = 16)
    axes.set_xlabel('Incident angle [deg]')
    axes.set_ylabel('Amplitude [dB]')   
    axes.axvline(linestyle = '--',linewidth = 2,color = 'black',x = theta_1)
    axes.axvline(linestyle = '--',linewidth = 2,color = 'black',x = theta_2)

    if alias_highlight:
       (theta_alias_min,theta_alias_max) = alias_border_calc(d)        
       print('Minimum alias angle %2.2f '%theta_alias_min)
       print('Maximum alias angle %2.2f '%theta_alias_max)
  	
       axes.axvspan(theta_alias_min, theta_alias_max, color='red', alpha=0.3) 
       axes.axvspan(180-theta_alias_min, 180, color='red', alpha=0.3) 
       
       axes.axvspan(180-theta_alias_min, 180-theta_alias_max, color='blue', alpha=0.3) 
       axes.axvspan(0, theta_alias_min, color='blue', alpha=0.3) 

    plt.grid()
    plt.show()   
    return axes

axes=plt.axes()
DOA_plot(Power, incident_angles, log_scale_min = -50, axes=axes, alias_highlight=False)
