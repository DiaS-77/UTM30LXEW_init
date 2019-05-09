import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from std_msgs.msg import String
import numpy as np

class station(object):
        def __init__(self, name):
	    rospy.init_node('UTM30LXEW', anonymous=True)
            self.tic = 0
	    self.toc = 0
	    self.acum = 0
	    self.acum2 = 0
	    self.new = 0
	    self.last = 1
	    self.total = 20
	    self.d = np.zeros([1,self.total+1])
	    self.ang = np.zeros([1,self.total+1])
	    self.main_station()

        def main_station(self):
            rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
            rospy.spin()

        def callback(self,data):
	    delta_hor_angle = data.angle_increment
	    max_hor_angle =   data.angle_max
	    min_hor_angle =   data.angle_min
	    ranges =          data.ranges
	    N = len(ranges)
	    D1 = N//2
	    D2 = D1+1
	    D3 = D2+1
	    theta = np.linspace(min_hor_angle,max_hor_angle,N)
	    #print str(N)+"\t"+str(D1)+"\t"+str(D2)+"\t"+str(D3)
	    ranges_0 = np.zeros([1,81])
	    sin_theta = np.sin(theta)
	    sin_angle_1 = sin_theta[D1-10]
            sin_angle_2 = sin_theta[D1+10]
	    #print str(sin_angle_1)+"\t"+str(sin_angle_2)
	    for k in range(0,81):
		aux = str(ranges[k+D1-39]).split("[")
		aux = str(aux[1]).strip("]")
		aux = aux.split(",")
		ranges_0[0,k] = float(aux[0])
	    #print ranges_0
	    w1=sin_angle_1*ranges_0[0,0]
	    w2=sin_angle_2*ranges_0[0,80]
	    #print str(w1)+"\t"+str(w2)
	    self.d[0,self.new] = (ranges_0[0,39]+ranges_0[0,40]+ranges_0[0,41])/3.0
	    self.ang[0,self.new] = w1+w2
	    self.acum += self.d[0,self.new]
	    self.acum -= self.d[0,self.last]
	    self.acum2 += self.ang[0,self.new]
	    self.acum2 -= self.ang[0,self.last]
	    #print str(self.acum)+"\t"+str(self.acum2)
	    #print str(self.new)+"\t"+str(self.last)
	    avg = self.acum/self.total
	    angle = self.acum2/self.total
	    angle *= 1000  # Guarantiees 3 digits of accuracy
	    #print "d = "+str(avg)+",\tE_angle = "+str(angle)
	    self.new += 1
	    self.last += 1
	    if  self.new == self.total:
		self.new = 0
	    if self.last == self.total:
		self.last = 0
	    pub1=rospy.Publisher('Distance',String,queue_size=1)
	    pub1.publish(str(avg))
	    pub2=rospy.Publisher('AngleError',String,queue_size=1)
	    pub2.publish(str(angle))


if __name__ == '__main__':
    hokuyo   = station('Station')
