import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import numpy as np

class station(object):
        def __init__(self, name):
	    rospy.init_node('Ocurence', anonymous=True)
	    self.d=0
	    self.cont=0
	    self.cont2=0
	    self.k=1000
	    self.flag=0
	    self.r=rospy.Rate(40)
	    self.ranges0 = np.zeros(self.k)
	    self.intensities0 = np.zeros(self.k)
	    self.header_concurrence()
	    self.concurrence()

	def header_concurrence(self):
	    rospy.sleep(4)
	    while self.flag == 0:
		node_distance = rospy.Subscriber('/Distance', String, self.header)
		self.r.sleep()

    	def header(self,data):
	    if self.d == 0:
		self.flag=1
	    	aux=':'
		D = str(data).split(aux)
		self.d = D[1]

	def concurrence(self):
	    global node_echo
	    rospy.loginfo("Starting node")
	    node_echo = rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
	    rospy.Subscriber('/joy', Joy, self.SaveData)
	    rospy.spin()
	    self.writeText()

	def callback(self,data):
	    if self.cont <= self.k:
		if self.cont == self.k:
		    self.flag = 2
		    node_echo.unregister()
		    rospy.signal_shutdown("stop spin")
		else:
		    #print self.cont
		    ranges =          data.ranges
		    intensities =     data.intensities
		    N = len(ranges)
		    D0 = N//2
		    aux = str(ranges[D0]).split("[")
		    aux = aux[1].strip("]")
		    self.ranges0[self.cont] = float(aux)
		    aux = str(intensities[D0]).split("[")
		    aux = aux[1].strip("]")
		    self.intensities0[self.cont] = float(aux)
		    #print aux
		    self.cont = self.cont+1

	def SaveData(self):
	    cont2 = cont2+1;
	    rospy.loginfo("Beginning mesurment...")
	    rospy.sleep(1.5)
	    file1 = open("concurrence.txt"+cont2, "w")
	    file1.write("#ranges"+"\t"+"Intensities \t para D= "+str(self.d)+"\n")
	    
	def writeText(self):
	    for i in range(0,self.k):
		file1.write(str(self.ranges0[i])+"\t"+str(self.intensities0[i])+"\n")
	    ranges_std = np.std(self.ranges0)
	    intensities_std = np.std(self.intensities0)
	    ranges_avg = np.mean(self.ranges0)
	    intensities_avg = np.mean(self.intensities0)
	    file1.write("#ranges_std: "+"\t"+str(ranges_std)+"\t"+", intensities_std: "+"\t"+str(intensities_std)+"\n")
	    file1.write("#ranges_aveg: "+"\t"+str(ranges_avg)+"\t"+", intensities_avg: "+"\t"+str(intensities_avg)+"\n")
	    rospy.loginfo("Mesurement finshed...\n"+"\tData:\n\t\tranges_std: "+str(ranges_std)+"\n\t\tintensities_std: "+str(intensities_std))
	    rospy.loginfo("\t\tranges_avg: "+str(ranges_avg)+"\n\t\tintensities_avg: "+str(intensities_avg))
	    file1.close()
	    exit()

if __name__ == '__main__':
    hokuyo   = station('Station')
