import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt

class station(object):
        def __init__(self, name):
            rospy.init_node('UTM30LXEW', anonymous=True)
	    self.tic = 0
	    self.toc = 0
	    self.file1 = 0
            self.main_station()

        def main_station(self):
	    self.file1 = open("Todo.txt", "a")
	    self.file1.write("#Angle"+"\t"+"Ranges"+"\n")
            rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
	    rospy.Subscriber('/joy',Joy,self.control)
            rospy.spin()

	def control(self,data):
	    butt = data.buttons
	    A = int(butt[0])
	    B = int(butt[1])
	    if (A & B):
		print "Hola"

        def callback(self,data):
	    self.tic = rospy.get_time()
	    delta_hor_angle = data.angle_increment
	    max_hor_angle =   data.angle_max
	    min_hor_angle =   data.angle_min
	    intensities =     data.intensities
	    ranges =          data.ranges
	    N = len(ranges)
	    theta = np.linspace(min_hor_angle,max_hor_angle,N)
	    ranges_0 = np.zeros([1,N])
	    ranges_1 = np.zeros([1,N])
	    ranges_2 = np.zeros([1,N])
	    intensities_0 = np.zeros([1,N])
            intensities_1 = np.zeros([1,N])
            intensities_2 = np.zeros([1,N])
	    for k in range(0,N):
		aux = str(ranges[k]).split("[")
		aux = str(aux[1]).strip("]")
		aux = aux.split(",")
		aux2 = str(intensities[k]).split("[")
                aux2 = str(aux2[1]).strip("]")
                aux2 = aux2.split(",")
		if len(aux)==1:
			ranges_0[0,k] = float(aux[0])
			intensities_0[0,k] = float(aux2[0])
		elif len(aux)==2:
			ranges_0[0,k] = float(aux[0])
			ranges_1[0,k] = float(aux[1])
			intensities_0[0,k] = float(aux2[0])
			intensities_1[0,k] = float(aux2[1])
		elif len(aux)==3:
			ranges_0[0,k] = float(aux[0])
			ranges_1[0,k] = float(aux[1])
			ranges_2[0,k] = float(aux[2])
			intensities_0[0,k] = float(aux2[0])
			intensities_1[0,k] = float(aux2[1])
			intensities_2[0,k] = float(aux2[2])
	    	self.file1.write(str(theta[k])+"\t"+str(ranges_0[0,k])+"\t"+str(ranges_1[0,k])+"\t"+str(ranges_2[0,k])+"\n")
	    self.toc=rospy.get_time()
	    rospy.loginfo("Time: "+str(self.toc-self.tic))
	    Xr_0 = np.cos(theta)*ranges_0[0,:]
	    Yr_0 = np.sin(theta)*ranges_0[0,:]
	    Xr_1 = np.cos(theta)*ranges_1[0,:]
            Yr_1 = np.sin(theta)*ranges_1[0,:]
	    Xr_2 = np.cos(theta)*ranges_2[0,:]
            Yr_2 = np.sin(theta)*ranges_2[0,:]
#	    plt.figure(1)
#	    plt.clf()
#	    plt.plot(Xr_0,Yr_0,'.',label="echoe 1")
#	    plt.plot(Xr_1,Yr_1,'o',label="echoe 2")
#	    plt.plot(Xr_2,Yr_2,'*',label="echoe 3")
#	    plt.legend()
#	    plt.show()
#	    plt.savefig('echoes_ranges.png')
#	    # Second Figure
#	    plt.figure(2)
#	    plt.clf()
#	    plt.scatter(Xr_0,Yr_0, s=0.5, c=intensities_0[0,:],label="echo 1")
#	    plt.scatter(Xr_1,Yr_1, s=0.5, c=intensities_1[0,:],label="echo 2")
#	    plt.scatter(Xr_2,Yr_2, s=0.5, c=intensities_2[0,:],label="echo 3")
#	    plt.colorbar()
#           plt.legend()
#           plt.show()
#           plt.savefig('echoes_intensities.png')

if __name__ == '__main__':
    hokuyo   = station('Station')
