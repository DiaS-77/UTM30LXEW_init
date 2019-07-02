import rospy
from std_msgs.msg import String
import numpy as np
import serial

class sensors(object):
        def __init__(self, name):
            rospy.init_node('Sensors', anonymous=True)
	    self.ser = serial.Serial('/dev/Sensors')  # open serial port
	    self.file1 = open("Sensors.txt", "w") 
            self.main_sensors()

        def main_sensors(self):
	    I=0
	    T=0
	    t=0
	    self.file1.write("I"+"\t"+"T\n") 
	    while not rospy.is_shutdown():
		line = self.ser.readline()
		#print line
		aux = line.split(";")
		#print aux
		if len(aux) == 3:
			if aux[0].find("$I") == 0:
			    aux1 = aux[0].split("I")
			    #print aux1[1]
			    I = float(aux1[1])
			if aux[1].find("T") == 0:
			    aux1 = aux[1].strip("T")
			    #print aux1
			    T = float(aux1)
			if aux[2].find("tms") == 0:
			    aux1 = aux[2].split("tms")
			    aux2 = aux1[1].split("$")
			    #print aux2[0]
			    t = float(aux2[0])/1000
			print "I = "+str(I)+",\tT = "+str(T)+",\tTs = "+str(t)
			self.file1.write(str(I)+"\t"+str(T)+"\n")
			pub1=rospy.Publisher('TemperatureCurrent',String,queue_size=1)
		    	pub1.publish("T:"+str(T)+"; I:"+str(I))
		    	pub3=rospy.Publisher('SampleTimeSensors',String,queue_size=1)
		    	pub3.publish("Ts:"+str(t))

if __name__ == '__main__':
    hokuyo   = sensors('sensors')
