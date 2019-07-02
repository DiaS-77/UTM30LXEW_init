import rospy
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import os.path
from os import path

class station(object):
        def __init__(self, name):
            rospy.init_node('UTM30LXEW', anonymous=True)
	    self.tic = 0
	    self.toc = 0
            self.main_station()

        def main_station(self):
	    avgR = 0
	    stdR = 0
	    avgI = 0
	    stdI = 0
	    #file1 = open("/home/sebastian/Documents/Data/10Jun/Temperature.txt", "r")
	    file1 = open("Temperature.txt", "r")
	    A = file1.readlines()
	    N = (len(A)-1)#-4000-880417
	    print N
	    ranges = np.zeros(N)
	    intensities = np.zeros(N)
	    T = np.zeros(N)
	    I = np.zeros(N)
	    t = np.linspace(0,(N-1)*0.025/60,N)
	    for k in range(1,N+1):
		B = A[k]
		aux = B.split("\t")
		T[k-1] = float(aux[0]);
		I[k-1] = float(aux[1]);
		ranges[k-1] = float(aux[3]);
		intensities[k-1] = float(aux[7]);
	    avgR = np.mean(ranges)
	    stdR = np.std(ranges)*1000
	    avgI = np.mean(intensities)
	    stdI = np.std(intensities)
	    plt.figure(1)
	    plt.clf()
	    plt.subplot(2,1,1)
	    plt.plot(t,ranges,'.')
	    plt.subplot(2,1,2)
	    plt.plot(t,intensities,'.')
#	    plt.show()
	    print avgR
	    plt.figure(2)
	    plt.clf()
	    plt.subplot(4,1,1);
	    plt.plot(ranges,'.',label="R")
	    plt.subplot(4,1,2);
	    plt.plot(intensities,'.',label="I")
	    plt.legend()
	    plt.subplot(4,1,3);
	    plt.plot(T,'.',label="T")
	    plt.legend()
	    plt.subplot(4,1,4);
	    plt.plot(I,'.',label="i")
	    plt.legend()
#	    plt.show()
	    plt.figure(3)
	    plt.clf()
	    plt.subplot(2,2,1);
	    plt.plot(T,ranges,'.',label="R_vs_T")
	    plt.legend()
	    plt.subplot(2,2,3);
	    plt.plot(T,intensities,'.',label="I_vs_T")
	    plt.legend()
	    plt.subplot(2,2,2);
	    plt.plot(I,ranges,'.',label="R_vs_i")
	    plt.legend()
	    plt.subplot(2,2,4);
	    plt.plot(I,intensities,'.',label="I_vs_i")
	    plt.legend()
	    plt.show()
	    exit()

if __name__ == '__main__':
    hokuyo   = station('Station')
