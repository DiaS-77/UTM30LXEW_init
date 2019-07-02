from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import os.path
from os import path

class station(object):
        def __init__(self, name):
	    self.tic = 0
	    self.toc = 0
	    self.k = 36
            self.main_station()

        def main_station(self):
	    avgR = np.zeros(self.k-1)
	    stdR = np.zeros(self.k-1)
	    avgI = np.zeros(self.k-1)
	    stdI = np.zeros(self.k-1)
	    for i in range(1,self.k):
		if path.exists("DataSet_"+str(i)+".txt"):
		    file1 = open("DataSet_"+str(i)+".txt", "r")
		    A = file1.readlines()
		    N = len(A)-1
		    #print N
		    ranges = np.zeros(N)
		    intensities = np.zeros(N)
		    for k in range(1,N+1):
			B = A[k]
			aux = B.split("\t")
			ranges[k-1] = float(aux[0]);
			intensities[k-1] = float(aux[1]);
		    avgR[i-1] = np.mean(ranges)
		    stdR[i-1] = np.std(ranges)*1000
		    avgI[i-1] = np.mean(intensities)
		    stdI[i-1] = np.std(intensities)
		    plt.figure(1)
		    plt.subplot(2,1,1)
		    plt.plot(ranges,'.')
		    plt.subplot(2,1,2)
		    plt.plot(intensities,'.')
#		    plt.show()
		else:
		    print "No existe DataSet_"+str(i)+".txt"
	    print avgR
	    plt.figure(2)
	    plt.clf()
	    plt.subplot(2,1,1);
	    plt.plot(avgR,stdI,'.',label="dispI")
	    plt.legend()
	    plt.subplot(2,1,2);
	    plt.plot(avgR,avgI,label="Intencities")
	    plt.legend()
	    plt.figure(3)
	    plt.clf()
	    plt.subplot(2,1,1);
	    plt.plot(avgR,stdR,'.',label="dispR")
	    plt.legend()
	    plt.subplot(2,1,2);
	    plt.plot(avgR,avgR,label="Ranges")
	    plt.legend()
	    plt.show()
	    exit()

if __name__ == '__main__':
    hokuyo   = station('Station')
