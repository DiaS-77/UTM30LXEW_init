import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import numpy as np

class station(object):
	def __init__(self, name):
	    rospy.init_node('Test', anonymous=True)
	    self.flag = 0
	    self.k=400	# Pruebas de 10 s
	    self.cont=2*self.k
	    self.cont2=0
	    self.file = 0
	    self.T = 0
	    self.ranges0 = np.zeros(self.k)
	    self.intensities0 = np.zeros(self.k)
	    self.main()

	def main(self):
	    rospy.sleep(2)
	    rospy.loginfo("Starting node")
	    rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
	    rospy.Subscriber('//TemperatureCurrent', String, self.Temperature)
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
		self.file = open("DataSet_"+str(self.cont2)+".txt", "w")
		self.file.write("#ranges"+"\t"+"Intensities"+"\t"+"Temperature"+"\n")

	def Temperature(self,data):
	    if self.cont <= self.k:
		aux=str(data).split(";")
		aux1=aux[0].split(":")
		aux2=aux[1].split(":")
		self.T = float(aux1[2].strip(" \" "))
		print str(self.T)

	def callback(self,data):
	    if self.cont <= self.k:
		if self.cont == self.k:
		    self.file.close()
		    self.cont = 2*self.k
		    self.flag = 0
		else:
		    ranges =          data.ranges
		    intensities =     data.intensities
		    N = len(ranges)
		    D0 = N//2
		    aux = str(ranges[D0]).split("[")
		    aux = aux[1].split(",")
		    aux = aux[0].strip("]")
		    F_rang = float(aux)
		    aux = str(intensities[D0]).split("[")
		    aux = aux[1].split(",")
		    aux = aux[0].strip("]")
		    F_int = float(aux)
		    self.file.write(str(F_rang)+"\t"+str(F_int)+"\t"+str(self.T)+"\n")
		    self.cont = self.cont+1
		    print str(self.cont)+"\t"+str(F_rang)

if __name__ == '__main__':
    hokuyo   = station('Station')
