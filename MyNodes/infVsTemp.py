import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from std_msgs.msg import String
import numpy as np

class station(object):
        def __init__(self, name):
	    rospy.init_node('infVsTemp', anonymous=True)
	    self.ranges0 = np.zeros(4)
	    self.intensities0 = np.zeros(4)
	    self.D = np.array([-3, 0, 3, -360])
	    self.flag = 0
	    self.T = 0
	    self.I = 0
	    self.file1 = open("Temperature.txt", "w")
	    self.file1.write("#Temp"+"\t"+"Current"+"\t"+"ranges"+"\t\t\t"+"Intensities"+"\t\t\t\n")
	    self.main()

	def main(self):
	    rospy.Subscriber('//TemperatureCurrent', String, self.callback1)
	    rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
            rospy.spin()

	def callback1(self,data):
	    if self.flag == 0:
		aux=str(data).split(";")
		aux1=aux[0].split(":")
#		print aux1
		aux2=aux[1].split(":")
#		print aux2
		self.T = float(aux1[2].strip(" \" "))
		self.I = float(aux2[1].strip('"'))
#		print str(self.T)+" "+str(self.I)
		self.flag = 1

	def callback(self,data):
	    if self.flag==1:
		ranges =          data.ranges
		intensities =     data.intensities
		N = len(ranges)
		D0 = N//2
		N = len(ranges)
		for i in range(0,len(self.D)):
		   aux = str(ranges[D0+self.D[i]]).split("[")
		   aux = aux[1].split(",")
		   aux = aux[0].strip("]")
		   self.ranges0[i] = float(aux)
		   aux = str(intensities[D0+self.D[i]]).split("[")
		   aux = aux[1].split(",")
		   aux = aux[0].strip("]")
		   self.intensities0[i] = float(aux)
		print self.ranges0[3]
		self.file1.write(str(self.T)+"\t"+str(self.I)+"\t"+str(self.ranges0[0])+"\t"+str(self.ranges0[1])+"\t"+str(self.ranges0[2])+"\t"+str(self.ranges0[3])+"\t"+str(self.intensities0[0])+"\t"+str(self.intensities0[1])+"\t"+str(self.intensities0[2])+"\t"+str(self.intensities0[3])+"\n")
		print str(self.T)+"\t"+str(self.I)+"\t"+str(self.ranges0[1])+"\t"+str(self.intensities0[1])+"\n"
		self.flag=0

if __name__ == '__main__':
    hokuyo   = station('Station')
