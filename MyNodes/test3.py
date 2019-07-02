import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt

class station(object):
	def __init__(self, name):
	    rospy.init_node('Test', anonymous=True)
	    self.flag = 0
	    self.k=400	# Pruebas de 10 s
	    self.cont=2*self.k
	    self.cont2=0
	    self.file1 = 0
	    self.file2 = 0
	    self.ranges_0 = np.zeros(1081)
	    self.ranges_1 = np.zeros(1081)
	    self.ranges_2 = np.zeros(1081)
	    self.intensities_0 = np.zeros(1081)
	    self.intensities_1 = np.zeros(1081)
	    self.intensities_2 = np.zeros(1081)
	    self.main()

	def main(self):
	    rospy.sleep(2)
	    rospy.loginfo("Starting node")
	    rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
	    rospy.Subscriber('/joy', Joy, self.SaveData)
	    rospy.spin()

	def SaveData(self,data):
	    key = data.buttons
	    A = int(key[0])
	    B = int(key[2])
	    if (A and B and self.flag == 0):
		self.cont2 = self.cont2+1
		rospy.loginfo("Beginning mesurment...")
		self.cont = 0
		self.flag = 1
		self.file1 = open("DataEcoRanges_"+str(self.cont2)+".txt", "w")
		self.file2 = open("DataEcoIntencities_"+str(self.cont2)+".txt", "w")

	def callback(self,data):
	    if self.cont <= self.k:
		ranges =          data.ranges
		intensities =     data.intensities
		max_hor_angle =   data.angle_max
		min_hor_angle =   data.angle_min
		N = len(ranges)
		D0 = N//2
		theta = np.linspace(min_hor_angle,max_hor_angle,N)
		if self.cont == self.k:
		    self.file1.close()
		    self.file2.close()
		    self.cont = 2*self.k
		    self.flag = 0
		    Xr_0 = np.cos(theta)*self.ranges_0[:]
		    Yr_0 = np.sin(theta)*self.ranges_0[:]
		    Xr_1 = np.cos(theta)*self.ranges_1[:]
		    Yr_1 = np.sin(theta)*self.ranges_1[:]
		    Xr_2 = np.cos(theta)*self.ranges_2[:]
		    Yr_2 = np.sin(theta)*self.ranges_2[:]
		    plt.figure(1)
		    plt.clf()
		    plt.plot(Xr_0,Yr_0,'.',label="echoe 1")
		    plt.plot(Xr_1,Yr_1,'o',label="echoe 2")
		    plt.plot(Xr_2,Yr_2,'*',label="echoe 3")
		    plt.legend()
		    plt.show()
		else:
		    for k in range(0,N):
			aux = str(ranges[k]).split("[")
			aux = str(aux[1]).strip("]")
			aux = aux.split(",")
			aux2 = str(intensities[k]).split("[")
			aux2 = str(aux2[1]).strip("]")
			aux2 = aux2.split(",")
			self.ranges_0[k] = float(aux[0])
			self.intensities_0[k] = float(aux2[0])
			if len(aux)==2:
			    self.ranges_1[k] = float(aux[1])
			    self.intensities_1[k] = float(aux2[1])
			elif len(aux)==3:
			    self.ranges_1[k] = float(aux[1])
			    self.ranges_2[k] = float(aux[2])
			    self.intensities_1[k] = float(aux2[1])
			    self.intensities_2[k] = float(aux2[2])
			self.file1.write(str(self.ranges_0[k])+"\t"+str(self.ranges_1[k])+"\t"+str(self.ranges_2[k]))
			self.file2.write(str(self.intensities_0[k])+"\t"+str(self.intensities_1[k])+"\t"+str(self.intensities_2[k]))
		    self.file1.write("\n")
		    self.file2.write("\n")
		    self.cont = self.cont+1
		    print str(self.cont)+"\t"+str(self.ranges_0[D0])

if __name__ == '__main__':
    hokuyo   = station('Station')
