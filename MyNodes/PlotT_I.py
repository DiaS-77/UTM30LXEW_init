from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import os.path
from os import path

class station(object):
        def __init__(self, name):
	    self.tic = 0
	    self.toc = 0
	    self.k = 22
            self.main_station()

        def main_station(self):
	    avgR = np.zeros(self.k-1)
	    stdR = np.zeros(self.k-1)
	    avgI = np.zeros(self.k-1)
	    stdI = np.zeros(self.k-1)
	    if path.exists("Temperature.txt"):
		file1 = open("Temperature.txt", "r")
		A = file1.readlines()
		N = len(A)-1
		ranges = np.zeros(N)
		intensities = np.zeros(N)
		T = np.zeros(N)
		I = np.zeros(N)
		for k in range(1,N+1):
		    B = A[k]
		    aux = B.split("\t")
		    T[k-1] = float(aux[0]);
		    I[k-1] = float(aux[1]);
		    ranges[k-1] = float(aux[2]);
		    intensities[k-1] = float(aux[3]);
		print T
#		avgR[i-1] = np.mean(ranges)
#		stdR[i-1] = np.std(ranges)*1000
#		avgI[i-1] = np.mean(intensities)
#		stdI[i-1] = np.std(intensities)
#		plt.figure(1)
#		plt.clf()
#		plt.subplot(2,1,1)
#		plt.plot(ranges,'.')
#		plt.subplot(2,1,2)
#		plt.plot(intensities,'.')
#		plt.legend()
#		plt.show()
	    plt.figure(2)
	    plt.clf()
	    plt.subplot(2,1,1);
	    plt.plot(T,ranges,'.',label="Ranges")
	    plt.legend()
	    plt.subplot(2,1,2);
	    plt.plot(T,intensities,'.',label="Intencities")
	    plt.legend()
	    plt.show()
	    exit()

if __name__ == '__main__':
    hokuyo   = station('Station')
