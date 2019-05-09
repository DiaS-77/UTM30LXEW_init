import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from std_msgs.msg import String
import numpy as np

class station(object):
        def __init__(self, name):
	    rospy.init_node('infVsTemp', anonymous=True)
	    self.flag=0
	    self.r=rospy.Rate(40)
	    self.ranges0 = 0
	    self.intensities0 = 0
	    self.main()

	def main(self):
	    rospy.Subscriber('/Temperature', String, self.callback1)
	    rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
            rospy.spin()

	def callback1(self,data):
	   if self.flag == 0:
		aux=str(data).split("T")
		aux=aux[1].split("&")
		self.I = float(aux[0])
		self.flag = 1
		print self.I

	def callback(self,data):
	    if self.flag == 1:
		ranges =          data.ranges
		intensities =     data.intensities
		N = len(ranges)
		D0 = N//2
		aux = str(ranges[D0]).split("[")
		aux = aux[1].split(",")
		aux = aux[0].strip("]")
		self.ranges0 = float(aux[0])
		aux = str(intensities[D0]).split("[")
		aux = aux[1].split(",")
		aux = aux[0].strip("]")
		self.intensities0 = float(aux[0])
		self.writeText();

	def writeText(self):
	    file1 = open("Temperature.txt", "a")
	    file1.write("#Temp"+"\t"+"ranges"+"\t"+"Intensities"+"\n")
	    file1.write(str(self.I)+"\t"+str(self.ranges0)+"\t"+str(self.intensities0)+"\n")
	    file1.close()
	    self.flag=0
	    

if __name__ == '__main__':
    hokuyo   = station('Station')
