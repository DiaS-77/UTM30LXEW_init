import rospy
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import os.path
from os import path

class station(object):
        def __init__(self, name):
	    self.tic = 0
	    self.toc = 0
	    self.k = 7
            self.main_station()

        def main_station(self):
	    avgR = np.zeros(self.k-1)
	    stdR = np.zeros(self.k-1)
	    avgI = np.zeros(self.k-1)
	    stdI = np.zeros(self.k-1)
	    for i in range(1,self.k):
		if path.exists("/home/sebastian/Documents/Data/Lux/DataSet_"+str(i+3)+".txt"):
		    file1 = open("/home/sebastian/Documents/Data/Lux/DataSet_"+str(i+3)+".txt", "r")
		    A = file1.readlines()
		    N = len(A)-1
		    #print N
		    ranges = np.zeros(N)
		    intensities = np.zeros(N)
		    L = np.array([526, 322, 0, 234, 234, 18, 18, 0, 0])
#		    L = np.array([234, 234, 18, 18, 0, 0])
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
		    plt.plot(ranges,'.',label="RANGES - "+str(L[i-1]))
		    plt.legend()
		    plt.subplot(2,1,2)
		    plt.plot(intensities,'.')
		    plt.legend()
#		    plt.show()
		else:
		    print "No existe DataSet_"+str(i)+".txt"
	    print avgR
	    print len(stdR)
	    plt.figure(2)
	    plt.clf()
#	    plt.subplot(2,2,1);
#	    plt.plot(L,avgR,'.',label="avg_Ranges")
#	    plt.legend()
	    plt.subplot(2,1,1);
	    plt.plot(L,stdR,'.',label="Ranges")
	    plt.legend()
#	    plt.subplot(2,2,3);
#	    plt.plot(L,avgI,'.',label="avg_Intencities")
#	    plt.legend()
	    plt.subplot(2,1,2);
	    plt.plot(L,stdI,'.',label="Intencities")
	    plt.legend()
	    plt.show()
	    exit()

if __name__ == '__main__':
    hokuyo   = station('Station')
