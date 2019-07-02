from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import os.path
from os import path

class station(object):
        def __init__(self, name):
	    self.tic = 0
	    self.toc = 0
            self.main_station()

        def main_station(self):
	    avgR = np.zeros(8)
	    stdR = np.zeros(8)
	    avgI = np.zeros(8)
	    stdI = np.zeros(8)
	    #file1 = open("/home/sebastian/Documents/Data/10Jun/Temperature.txt", "r")
	    file1 = open("Temperature.txt", "r")
	    file2 = open("Temperature2.txt", "r")
	    A = file1.readlines()
	    A2 = file2.readlines()
	    N = min((len(A)-1),(len(A2)-1))
	    print N
	    ranges = np.zeros([8,N])
	    intensities = np.zeros([8,N])
	    T = np.zeros([2,N])
	    I = np.zeros([2,N])
	    t = np.linspace(0,(N-1)*0.025/60,N)
	    for j in range(0,4):
		for k in range(1,N+1):
		    B = A[k]
		    aux = B.split("\t")
		    T[0,k-1] = float(aux[0]);
		    I[0,k-1] = float(aux[1]);
		    ranges[j,k-1] = float(aux[2]);
		    intensities[j,k-1] = float(aux[6])
		    B = A2[k]
		    aux = B.split("\t")
		    T[1,k-1] = float(aux[0]);
		    I[1,k-1] = float(aux[1]);
		    ranges[j+4,k-1] = float(aux[2]);
		    intensities[j+4,k-1] = float(aux[6])
		[avgR[j],avgR[j+4]] = np.array([np.mean(ranges[j,:]),np.mean(ranges[j+4])])
		[stdR[j],stdR[j+4]] = np.array([np.std(ranges[j,:]),np.std(ranges[j+4])])*1000
		[avgI[j],avgI[j+4]] = np.array([np.mean(intensities[j,:]),np.mean(intensities[j+4])])
		[stdI[j],stdI[j+4]] = np.array([np.std(intensities[j,:]),np.std(intensities[j+4])])
		plt.figure(1)
		plt.subplot(2,1,1)
		plt.plot(t,ranges[j,:],'.',label=str(avgR[j])+"m")
		plt.plot(t,ranges[j+4,:],'.',label=str(avgR[j+4])+"m")
		plt.legend()
		plt.subplot(2,1,2)
		plt.plot(t,intensities[j,:],'.')
		print avgR[j]
		plt.figure(2)
		plt.subplot(3,1,1);
		plt.plot(t,ranges[j,:],'.',label=str(avgR[j])+"m")
		plt.plot(t,ranges[j+4,:],'.',label=str(avgR[j+4])+"m")
		plt.legend()
		plt.subplot(3,1,2);
		plt.plot(t,intensities[j,:],'.',label="I1")
		plt.legend()
		plt.subplot(3,1,3);
		plt.plot(t,T[0],'.',label="T2")
		plt.plot(t,T[1],'.',label="T1")
		plt.legend()
	    plt.show()
	    exit()

if __name__ == '__main__':
    hokuyo   = station('Station')
